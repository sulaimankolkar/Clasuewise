"""
Clause extraction and segmentation utilities
"""

import re
from typing import List, Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClauseExtractor:
    """Extract and segment clauses from legal documents"""
    
    def __init__(self):
        """Initialize the clause extractor"""
        logger.info("Clause extractor initialized")
    
    def extract_clauses(self, text: str) -> List[Dict[str, any]]:
        """Extract individual clauses from legal document"""
        # Clean and preprocess text
        text = self._preprocess_text(text)
        
        # Split into sections first
        sections = self._split_into_sections(text)
        
        clauses = []
        clause_id = 1
        
        for section_idx, section in enumerate(sections):
            section_clauses = self._extract_clauses_from_section(section, section_idx + 1)
            
            for clause_text in section_clauses:
                clause = {
                    'id': clause_id,
                    'section': section_idx + 1,
                    'text': clause_text.strip(),
                    'type': self._classify_clause_type(clause_text),
                    'length': len(clause_text.split()),
                    'complexity': self._assess_complexity(clause_text)
                }
                clauses.append(clause)
                clause_id += 1
        
        return clauses
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess the text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common OCR errors
        text = text.replace('�', ' ')
        text = text.replace('\x00', ' ')
        
        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        return text.strip()
    
    def _split_into_sections(self, text: str) -> List[str]:
        """Split document into logical sections"""
        # Common section patterns in legal documents
        section_patterns = [
            r'\n\s*(?:SECTION|Section|Article|ARTICLE)\s+\d+',
            r'\n\s*\d+\.\s+[A-Z][^.]{10,50}',
            r'\n\s*[A-Z][A-Z\s]{10,50}:',
            r'\n\s*(?:WHEREAS|THEREFORE|NOW THEREFORE)',
            r'\n\s*(?:Definitions|Obligations|Terms|Conditions|Termination|Confidentiality)'
        ]
        
        # Try to split by section headers
        for pattern in section_patterns:
            sections = re.split(pattern, text, flags=re.IGNORECASE)
            if len(sections) > 1:
                return [section.strip() for section in sections if section.strip()]
        
        # If no clear sections, split by paragraphs
        paragraphs = text.split('\n\n')
        return [p.strip() for p in paragraphs if len(p.strip()) > 50]
    
    def _extract_clauses_from_section(self, section: str, section_num: int) -> List[str]:
        """Extract clauses from a section"""
        # Split by sentence first (simple approach)
        sentences = self._simple_sentence_split(section)
        
        clauses = []
        current_clause = ""
        
        for sentence in sentences:
            # Check if this sentence starts a new clause
            if self._is_clause_boundary(sentence):
                if current_clause.strip():
                    clauses.append(current_clause.strip())
                current_clause = sentence
            else:
                current_clause += " " + sentence
        
        # Add the last clause
        if current_clause.strip():
            clauses.append(current_clause.strip())
        
        # Filter out very short clauses
        clauses = [clause for clause in clauses if len(clause.split()) > 5]
        
        return clauses
    
    def _is_clause_boundary(self, sentence: str) -> bool:
        """Determine if a sentence starts a new clause"""
        clause_starters = [
            r'^\s*\d+\.',  # Numbered clauses
            r'^\s*\([a-z]\)',  # Lettered sub-clauses
            r'^\s*(?:The|Each|Any|All|No)\s+(?:Party|Parties|Company|Employee)',
            r'^\s*(?:Upon|In the event|If|When|Unless|Provided that)',
            r'^\s*(?:Notwithstanding|Subject to|Except as)',
            r'^\s*(?:Party|Parties|Company|Employee|Contractor)\s+(?:shall|will|must|agrees)'
        ]
        
        for pattern in clause_starters:
            if re.match(pattern, sentence, re.IGNORECASE):
                return True
        
        return False
    
    def _classify_clause_type(self, clause_text: str) -> str:
        """Classify the type of clause"""
        clause_text_lower = clause_text.lower()
        
        # Define clause type patterns
        clause_types = {
            'Confidentiality': ['confidential', 'non-disclosure', 'proprietary', 'trade secret'],
            'Termination': ['terminate', 'termination', 'end', 'expire', 'dissolution'],
            'Payment': ['payment', 'pay', 'compensation', 'salary', 'fee', 'remuneration'],
            'Obligation': ['shall', 'must', 'required', 'obligated', 'responsible'],
            'Liability': ['liable', 'liability', 'damages', 'indemnify', 'indemnification'],
            'Intellectual Property': ['intellectual property', 'copyright', 'trademark', 'patent'],
            'Jurisdiction': ['jurisdiction', 'governing law', 'court', 'dispute resolution'],
            'Definition': ['means', 'defined as', 'refers to', 'definition'],
            'Warranty': ['warrant', 'warranty', 'guarantee', 'represent'],
            'Force Majeure': ['force majeure', 'act of god', 'unforeseeable']
        }
        
        for clause_type, keywords in clause_types.items():
            if any(keyword in clause_text_lower for keyword in keywords):
                return clause_type
        
        return 'General'
    
    def _assess_complexity(self, clause_text: str) -> str:
        """Assess the complexity of a clause"""
        word_count = len(clause_text.split())
        sentences = self._simple_sentence_split(clause_text)
        sentence_count = len(sentences)
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        # Count complex legal terms
        complex_terms = [
            'notwithstanding', 'heretofore', 'hereinafter', 'whereas', 'thereof',
            'indemnification', 'subrogation', 'covenant', 'estoppel', 'severability'
        ]
        complex_term_count = sum(1 for term in complex_terms if term in clause_text.lower())
        
        # Assess complexity
        if word_count > 100 or avg_sentence_length > 25 or complex_term_count > 2:
            return 'High'
        elif word_count > 50 or avg_sentence_length > 15 or complex_term_count > 0:
            return 'Medium'
        else:
            return 'Low'
    
    def get_clause_statistics(self, clauses: List[Dict]) -> Dict:
        """Get statistics about extracted clauses"""
        if not clauses:
            return {}
        
        total_clauses = len(clauses)
        clause_types = {}
        complexity_counts = {'Low': 0, 'Medium': 0, 'High': 0}
        total_words = 0
        
        for clause in clauses:
            # Count clause types
            clause_type = clause.get('type', 'General')
            clause_types[clause_type] = clause_types.get(clause_type, 0) + 1
            
            # Count complexity
            complexity = clause.get('complexity', 'Low')
            complexity_counts[complexity] += 1
            
            # Count words
            total_words += clause.get('length', 0)
        
        avg_words_per_clause = total_words / total_clauses if total_clauses > 0 else 0
        
        return {
            'total_clauses': total_clauses,
            'clause_types': clause_types,
            'complexity_distribution': complexity_counts,
            'average_words_per_clause': round(avg_words_per_clause, 1),
            'total_words': total_words
        }
    
    def _simple_sentence_split(self, text: str) -> List[str]:
        """Simple sentence splitting without NLTK"""
        # Split on periods, exclamation marks, and question marks
        # But be careful about abbreviations and decimals
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\!|\?)\s+', text)
        
        # Clean up sentences
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # Ignore very short fragments
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences
