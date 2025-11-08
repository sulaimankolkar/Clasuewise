"""
Main ClauseWise analyzer that orchestrates all components
"""

from models.simple_model import SimpleModel
from utils.document_processor import DocumentProcessor
from utils.clause_extractor import ClauseExtractor
from typing import Dict, List, Any, Optional
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClauseWiseAnalyzer:
    """Main analyzer class that coordinates all AI models and utilities"""
    
    def __init__(self):
        """Initialize all components"""
        logger.info("Initializing ClauseWise Analyzer...")
        
        try:
            # Use simple rule-based model for immediate functionality
            logger.info("Loading simple rule-based model...")
            self.ai_model = SimpleModel()
            self.model_type = "simple"
            logger.info("Simple model loaded successfully")
            
            # Skip NER model to avoid spaCy loading issues
            self.ner_model = None
            self.clause_extractor = ClauseExtractor()
            self.document_processor = DocumentProcessor()
            
            logger.info("ClauseWise Analyzer initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing ClauseWise Analyzer: {e}")
            raise
    
    def analyze_document(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Complete analysis of a legal document"""
        logger.info(f"Starting analysis of document: {filename}")
        
        try:
            # Step 1: Extract text from document
            file_type = '.' + filename.split('.')[-1].lower()
            document_text = self.document_processor.process_document(file_content, file_type)
            
            if not document_text.strip():
                raise ValueError("No text could be extracted from the document")
            
            # Step 2: Basic document info
            doc_info = self.document_processor.get_file_info(file_content, filename)
            
            # Step 3: Document classification
            doc_classification = self.ai_model.classify_document(document_text)
            
            # Step 4: Extract clauses
            clauses = self.clause_extractor.extract_clauses(document_text)
            clause_stats = self.clause_extractor.get_clause_statistics(clauses)
            
            # Step 5: Simple Entity Recognition (regex-based)
            entities = self._extract_entities_simple(document_text)
            
            # Step 6: Generate document summary
            summary = self.ai_model.generate_summary(document_text)
            
            # Step 7: Extract key obligations
            obligations = self.ai_model.extract_obligations(document_text)
            
            # Compile results
            analysis_results = {
                'document_info': doc_info,
                'classification': doc_classification,
                'summary': summary,
                'text_length': len(document_text),
                'word_count': len(document_text.split()),
                'clauses': clauses,
                'clause_statistics': clause_stats,
                'entities': entities,
                'obligations': obligations,
                'raw_text': document_text[:1000] + "..." if len(document_text) > 1000 else document_text
            }
            
            logger.info(f"Document analysis completed successfully for: {filename}")
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error analyzing document {filename}: {e}")
            raise Exception(f"Analysis failed: {str(e)}")
    
    def simplify_clause(self, clause_text: str) -> str:
        """Simplify a specific clause"""
        try:
            return self.ai_model.simplify_clause(clause_text)
        except Exception as e:
            logger.error(f"Error simplifying clause: {e}")
            return f"Error: Could not simplify clause - {str(e)}"
    
    def extract_entities_from_text(self, text: str) -> Dict[str, List[str]]:
        """Extract entities from arbitrary text"""
        try:
            return self._extract_entities_simple(text)
        except Exception as e:
            logger.error(f"Error extracting entities: {e}")
            return {}
    
    def classify_text(self, text: str) -> str:
        """Classify document type from text"""
        try:
            return self.ai_model.classify_document(text)
        except Exception as e:
            logger.error(f"Error classifying text: {e}")
            return "Unknown"
    
    def get_analysis_summary(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Get a high-level summary of analysis results"""
        try:
            clause_stats = analysis_results.get('clause_statistics', {})
            entities = analysis_results.get('entities', {})
            
            # Count total entities
            total_entities = sum(len(entity_list) for entity_list in entities.values())
            
            # Get most common clause type
            clause_types = clause_stats.get('clause_types', {})
            most_common_clause = max(clause_types.items(), key=lambda x: x[1])[0] if clause_types else "Unknown"
            
            summary = {
                'document_type': analysis_results.get('classification', 'Unknown'),
                'total_clauses': clause_stats.get('total_clauses', 0),
                'total_entities': total_entities,
                'most_common_clause_type': most_common_clause,
                'complexity_high': clause_stats.get('complexity_distribution', {}).get('High', 0),
                'total_obligations': len(analysis_results.get('obligations', [])),
                'word_count': analysis_results.get('word_count', 0)
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating analysis summary: {e}")
            return {}
    
    def batch_simplify_clauses(self, clauses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Simplify multiple clauses"""
        simplified_clauses = []
        
        for clause in clauses:
            try:
                simplified_text = self.simplify_clause(clause['text'])
                simplified_clause = clause.copy()
                simplified_clause['simplified_text'] = simplified_text
                simplified_clauses.append(simplified_clause)
            except Exception as e:
                logger.error(f"Error simplifying clause {clause.get('id', 'unknown')}: {e}")
                simplified_clause = clause.copy()
                simplified_clause['simplified_text'] = "Error: Could not simplify this clause"
                simplified_clauses.append(simplified_clause)
        
        return simplified_clauses
    
    def _extract_entities_simple(self, text: str) -> Dict[str, List[str]]:
        """Simple regex-based entity extraction"""
        entities = {
            "PARTIES": [],
            "DATES": [],
            "MONEY": [],
            "ORGANIZATIONS": [],
            "LOCATIONS": [],
            "LEGAL_TERMS": [],
            "OBLIGATIONS": []
        }
        
        # Extract dates
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'
        ]
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["DATES"].extend(matches)
        
        # Extract money
        money_patterns = [
            r'\$[\d,]+\.?\d*',
            r'USD\s*[\d,]+\.?\d*',
            r'\b\d+\s*dollars?\b'
        ]
        for pattern in money_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["MONEY"].extend(matches)
        
        # Extract organizations (simple patterns)
        org_patterns = [
            r'\b[A-Z][a-z]+\s+(?:Inc|LLC|Corp|Corporation|Company|Ltd)\b',
            r'\b(?:Company|Corporation|LLC|Inc)\b'
        ]
        for pattern in org_patterns:
            matches = re.findall(pattern, text)
            entities["ORGANIZATIONS"].extend(matches)
        
        # Extract legal terms
        legal_terms = [
            'confidential', 'proprietary', 'intellectual property', 'copyright', 
            'trademark', 'patent', 'liability', 'indemnification', 'termination',
            'breach', 'covenant', 'warranty', 'jurisdiction', 'governing law'
        ]
        for term in legal_terms:
            if term.lower() in text.lower():
                entities["LEGAL_TERMS"].append(term)
        
        # Extract obligations
        obligation_patterns = [
            r'(?:shall|must|will|agrees to|required to|responsible for)\s+[^.]{10,100}'
        ]
        for pattern in obligation_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["OBLIGATIONS"].extend([match.strip() for match in matches])
        
        # Remove duplicates and limit results
        for key in entities:
            entities[key] = list(set(entities[key]))[:10]  # Limit to 10 items each
        
        return entities
