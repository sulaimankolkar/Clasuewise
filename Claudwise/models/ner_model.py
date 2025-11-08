"""
Named Entity Recognition for legal documents
"""

import spacy
from typing import List, Dict, Any
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LegalNER:
    def __init__(self, model_name: str = "en_core_web_sm"):
        """Initialize the NER model"""
        self.model_name = model_name
        self.nlp = None
        self._load_model()
    
    def _load_model(self):
        """Load the spaCy model"""
        try:
            logger.info(f"Loading spaCy model: {self.model_name}")
            self.nlp = spacy.load(self.model_name)
            logger.info("spaCy model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading spaCy model: {e}")
            raise
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract legal entities from text"""
        doc = self.nlp(text)
        
        entities = {
            "PARTIES": [],
            "DATES": [],
            "MONEY": [],
            "ORGANIZATIONS": [],
            "LOCATIONS": [],
            "LEGAL_TERMS": [],
            "OBLIGATIONS": []
        }
        
        # Standard spaCy entities
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG"]:
                if ent.label_ == "PERSON":
                    entities["PARTIES"].append(ent.text)
                else:
                    entities["ORGANIZATIONS"].append(ent.text)
            elif ent.label_ == "DATE":
                entities["DATES"].append(ent.text)
            elif ent.label_ == "MONEY":
                entities["MONEY"].append(ent.text)
            elif ent.label_ in ["GPE", "LOC"]:
                entities["LOCATIONS"].append(ent.text)
        
        # Custom legal entity extraction
        entities.update(self._extract_legal_entities(text))
        
        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities
    
    def _extract_legal_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract custom legal entities using regex patterns"""
        legal_entities = {
            "LEGAL_TERMS": [],
            "OBLIGATIONS": []
        }
        
        # Legal terms patterns
        legal_terms_patterns = [
            r'\b(?:agreement|contract|clause|provision|term|condition|covenant|warranty|indemnity|liability|breach|termination|confidentiality|non-disclosure|intellectual property|copyright|trademark|patent)\b',
            r'\b(?:shall|must|will|agrees to|obligated to|required to|responsible for|liable for)\b',
            r'\b(?:jurisdiction|governing law|dispute resolution|arbitration|mediation|litigation)\b'
        ]
        
        for pattern in legal_terms_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            legal_entities["LEGAL_TERMS"].extend(matches)
        
        # Obligation patterns
        obligation_patterns = [
            r'(?:shall|must|will|agrees to|is obligated to|is required to|is responsible for)\s+[^.]{10,100}',
            r'(?:Party|Parties|Company|Employee|Contractor|Licensee|Licensor)\s+(?:shall|must|will|agrees to)[^.]{10,100}'
        ]
        
        for pattern in obligation_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            legal_entities["OBLIGATIONS"].extend([match.strip() for match in matches])
        
        return legal_entities
    
    def extract_dates(self, text: str) -> List[str]:
        """Extract dates using regex patterns"""
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
            r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b'
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)
        
        return list(set(dates))
    
    def extract_monetary_values(self, text: str) -> List[str]:
        """Extract monetary values using regex patterns"""
        money_patterns = [
            r'\$[\d,]+\.?\d*',
            r'USD\s*[\d,]+\.?\d*',
            r'(?:dollars?|USD)\s*[\d,]+\.?\d*',
            r'[\d,]+\.?\d*\s*(?:dollars?|USD)'
        ]
        
        money = []
        for pattern in money_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            money.extend(matches)
        
        return list(set(money))
    
    def extract_parties(self, text: str) -> List[str]:
        """Extract party names from legal documents"""
        # Look for common party designation patterns
        party_patterns = [
            r'(?:Party|Parties):\s*([^.\n]+)',
            r'between\s+([^,\n]+)\s+and\s+([^,\n]+)',
            r'(?:Company|Corporation|LLC|Inc\.?|Ltd\.?):\s*([^.\n]+)',
            r'(?:Employee|Contractor|Individual):\s*([^.\n]+)'
        ]
        
        parties = []
        for pattern in party_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if isinstance(matches[0], tuple) if matches else False:
                for match_group in matches:
                    parties.extend(match_group)
            else:
                parties.extend(matches)
        
        # Clean up party names
        cleaned_parties = []
        for party in parties:
            party = party.strip().strip(',').strip()
            if len(party) > 2 and party not in cleaned_parties:
                cleaned_parties.append(party)
        
        return cleaned_parties
