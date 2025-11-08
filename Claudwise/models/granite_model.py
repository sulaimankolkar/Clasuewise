"""
IBM Granite model integration for legal document analysis
"""

from transformers import pipeline
import torch
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GraniteModel:
    def __init__(self, model_name: str = "ibm-granite/granite-3.2-2b-instruct"):
        """Initialize the Granite model pipeline"""
        self.model_name = model_name
        self.pipe = None
        self._load_model()
    
    def _load_model(self):
        """Load the Granite model pipeline"""
        try:
            logger.info(f"Loading Granite model: {self.model_name}")
            # Use CPU and smaller precision for faster loading
            self.pipe = pipeline(
                "text-generation", 
                model=self.model_name,
                torch_dtype=torch.float32,
                device_map=None,  # Force CPU for initial loading
                model_kwargs={"low_cpu_mem_usage": True}
            )
            logger.info("Granite model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading Granite model: {e}")
            # If the specific model fails, provide a fallback message
            logger.info("Note: First-time model download may take several minutes")
            raise
    
    def simplify_clause(self, clause: str, simplify_level: str = "basic") -> str:
        """Simplify a legal clause into layman-friendly language"""
        
        # Base prompt for clearer, more detailed outputs
        base_prompt = f"""You are an expert legal assistant helping non-lawyers understand legal clauses.
Rewrite the following legal clause in clear, plain, everyday English.
- Keep every important detail and meaning.
- Use natural phrasing instead of legal jargon.
- Explain terms simply if needed.
- Use 2–3 complete sentences.
- Avoid shortening too much.
- The goal is clarity, not brevity.

Clause:
{clause}

Rewritten Clause:"""

        # Add detailed instruction if requested
        if simplify_level == "detailed":
            base_prompt += "\nIf simplify_level is 'detailed', include short clarifying phrases to explain key terms."
        
        messages = [
            {
                "role": "user", 
                "content": base_prompt
            }
        ]
        
        try:
            result = self.pipe(
                messages, 
                max_new_tokens=250, 
                temperature=0.85,
                top_p=0.9,
                repetition_penalty=1.05,
                do_sample=True
            )
            simplified = result[0]['generated_text'][-1]['content']
            return simplified.strip()
        except Exception as e:
            logger.error(f"Error simplifying clause: {e}")
            return f"Error: Could not simplify clause - {str(e)}"
    
    def classify_document(self, document_text: str) -> str:
        """Classify the type of legal document"""
        messages = [
            {
                "role": "user",
                "content": f"""Analyze the following legal document and classify it into one of these categories:
- Non-Disclosure Agreement (NDA)
- Employment Contract
- Service Agreement  
- Lease Agreement
- Purchase Agreement
- Partnership Agreement
- License Agreement
- Other

Document text: {document_text[:1000]}...

Classification:"""
            }
        ]
        
        try:
            result = self.pipe(messages, max_new_tokens=50, temperature=0.1)
            classification = result[0]['generated_text'][-1]['content']
            return classification.strip()
        except Exception as e:
            logger.error(f"Error classifying document: {e}")
            return "Other"
    
    def extract_obligations(self, text: str) -> List[str]:
        """Extract key obligations from legal text"""
        messages = [
            {
                "role": "user",
                "content": f"""Extract all key obligations, duties, and responsibilities from the following legal text. List them as bullet points:

Legal Text: {text}

Key Obligations:"""
            }
        ]
        
        try:
            result = self.pipe(messages, max_new_tokens=300, temperature=0.3)
            obligations_text = result[0]['generated_text'][-1]['content']
            
            # Parse bullet points
            obligations = []
            for line in obligations_text.split('\n'):
                line = line.strip()
                if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                    obligations.append(line[1:].strip())
            
            return obligations
        except Exception as e:
            logger.error(f"Error extracting obligations: {e}")
            return []
    
    def generate_summary(self, document_text: str) -> str:
        """Generate a summary of the legal document"""
        messages = [
            {
                "role": "user",
                "content": f"""Provide a concise summary of this legal document, highlighting the key points, parties involved, and main terms:

Document: {document_text[:1500]}...

Summary:"""
            }
        ]
        
        try:
            result = self.pipe(messages, max_new_tokens=250, temperature=0.3)
            summary = result[0]['generated_text'][-1]['content']
            return summary.strip()
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return "Error: Could not generate summary"
