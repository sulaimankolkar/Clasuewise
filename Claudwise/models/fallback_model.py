"""
Fallback model for when Granite model is not available
Uses a smaller, faster model for demonstration
"""

from transformers import pipeline
import torch
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FallbackModel:
    """Lightweight fallback model for legal document analysis"""
    
    def __init__(self):
        """Initialize with a smaller, faster model"""
        self.model_name = "microsoft/DialoGPT-small"  # Much smaller model
        self.pipe = None
        self._load_model()
    
    def _load_model(self):
        """Load a smaller model for faster initialization"""
        try:
            logger.info(f"Loading fallback model: {self.model_name}")
            # Use a much smaller model that downloads quickly
            self.pipe = pipeline(
                "text-generation", 
                model="gpt2",  # Very small and fast
                max_length=200,
                pad_token_id=50256
            )
            logger.info("Fallback model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading fallback model: {e}")
            self.pipe = None
    
    def simplify_clause(self, clause: str) -> str:
        """Simplify a legal clause using the fallback model"""
        if not self.pipe:
            return "Model not available. Please try: This clause means that both parties agree to keep information confidential and not share it with others."
        
        try:
            # Simple prompt for the smaller model
            prompt = f"Simplify this legal text: {clause[:200]}... In simple terms:"
            result = self.pipe(prompt, max_length=150, num_return_sequences=1, temperature=0.7)
            
            if result and len(result) > 0:
                generated = result[0]['generated_text']
                # Extract only the simplified part
                if "In simple terms:" in generated:
                    simplified = generated.split("In simple terms:")[-1].strip()
                    return simplified if simplified else "This clause establishes legal obligations between the parties involved."
            
            return "This clause establishes legal obligations between the parties involved."
            
        except Exception as e:
            logger.error(f"Error simplifying clause: {e}")
            return "This clause contains important legal terms that define responsibilities and obligations for all parties involved."
    
    def classify_document(self, document_text: str) -> str:
        """Classify document type using simple keyword matching"""
        text_lower = document_text.lower()
        
        # Simple keyword-based classification
        if any(word in text_lower for word in ['non-disclosure', 'confidential', 'proprietary', 'nda']):
            return "Non-Disclosure Agreement (NDA)"
        elif any(word in text_lower for word in ['employment', 'employee', 'job', 'salary', 'work']):
            return "Employment Contract"
        elif any(word in text_lower for word in ['service', 'services', 'provide', 'deliver']):
            return "Service Agreement"
        elif any(word in text_lower for word in ['lease', 'rent', 'rental', 'tenant', 'landlord']):
            return "Lease Agreement"
        elif any(word in text_lower for word in ['purchase', 'buy', 'sale', 'sell']):
            return "Purchase Agreement"
        elif any(word in text_lower for word in ['partnership', 'partner', 'joint']):
            return "Partnership Agreement"
        elif any(word in text_lower for word in ['license', 'licensing', 'permit']):
            return "License Agreement"
        else:
            return "Other"
    
    def extract_obligations(self, text: str) -> List[str]:
        """Extract obligations using keyword patterns"""
        obligations = []
        
        # Simple pattern matching for obligations
        obligation_patterns = [
            "shall not",
            "must not", 
            "will not",
            "agrees to",
            "responsible for",
            "obligated to",
            "required to"
        ]
        
        sentences = text.split('.')
        for sentence in sentences[:10]:  # Limit to first 10 sentences
            sentence = sentence.strip()
            if any(pattern in sentence.lower() for pattern in obligation_patterns):
                if len(sentence) > 20 and len(sentence) < 200:
                    obligations.append(sentence + ".")
        
        return obligations[:5]  # Return max 5 obligations
    
    def generate_summary(self, document_text: str) -> str:
        """Generate a simple summary"""
        doc_type = self.classify_document(document_text)
        word_count = len(document_text.split())
        
        return f"This appears to be a {doc_type} containing approximately {word_count} words. The document establishes legal relationships and obligations between the parties involved. Key terms and conditions are outlined to govern the agreement."
