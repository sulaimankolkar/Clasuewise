"""
Simple rule-based model that works without any downloads
"""

import re
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleModel:
    """Rule-based model that requires no downloads"""
    
    def __init__(self):
        """Initialize with no external dependencies"""
        logger.info("Simple rule-based model initialized")
    
    def simplify_clause(self, clause: str) -> str:
        """Simplify a legal clause using rule-based approach"""
        try:
            # Basic simplification rules
            simplified = clause.strip()
            
            # Replace complex legal terms with simpler ones
            replacements = {
                r'\bheretofore\b': 'before this',
                r'\bhereinafter\b': 'from now on', 
                r'\bhereafter\b': 'after this',
                r'\bwhereas\b': 'since',
                r'\bthereof\b': 'of it',
                r'\btherein\b': 'in it',
                r'\bhereby\b': 'by this document',
                r'\bnotwithstanding\b': 'despite',
                r'\bpursuant to\b': 'according to',
                r'\bin consideration of\b': 'in exchange for',
                r'\bshall\b': 'must',
                r'\bshall not\b': 'cannot',
                r'\bmay not\b': 'cannot',
                r'\bparty of the first part\b': 'the first party',
                r'\bparty of the second part\b': 'the second party',
                r'\bindemnify and hold harmless\b': 'protect from any legal claims or damages',
                r'\bforce majeure\b': 'uncontrollable events (like natural disasters)',
                r'\bforthwith\b': 'immediately',
                r'\bwherein\b': 'where',
                r'\bwhereby\b': 'by which',
                r'\baforesaid\b': 'mentioned above',
                r'\bsubsequent to\b': 'after',
                r'\bprior to\b': 'before',
                r'\bin perpetuity\b': 'forever',
                r'\bterminate forthwith\b': 'end immediately',
                r'\brender null and void\b': 'cancel completely'
            }
            
            # Apply replacements
            for pattern, replacement in replacements.items():
                simplified = re.sub(pattern, replacement, simplified, flags=re.IGNORECASE)
            
            # Break down complex sentences
            if len(simplified) > 150:
                # Try to split long sentences at conjunctions
                if ' and ' in simplified and len(simplified.split(' and ')) == 2:
                    parts = simplified.split(' and ')
                    simplified = f"{parts[0].strip()}. Additionally, {parts[1].strip()}"
                elif ' but ' in simplified:
                    parts = simplified.split(' but ')
                    simplified = f"{parts[0].strip()}. However, {parts[1].strip()}"
            
            # Add clear explanation
            if 'must' in simplified.lower() or 'cannot' in simplified.lower():
                prefix = "**Key Requirement:** "
            elif 'protect' in simplified.lower() or 'confidential' in simplified.lower():
                prefix = "**Protection Clause:** "
            elif 'payment' in simplified.lower() or 'pay' in simplified.lower() or '$' in simplified:
                prefix = "**Payment Terms:** "
            elif 'terminate' in simplified.lower() or 'end' in simplified.lower():
                prefix = "**Termination Clause:** "
            else:
                prefix = "**In Plain English:** "
            
            return f"{prefix}{simplified}"
                
        except Exception as e:
            logger.error(f"Error in simplification: {e}")
            return "**Summary:** This clause establishes important legal obligations and rights between the parties involved."
    
    def classify_document(self, document_text: str) -> str:
        """Classify document type using keyword matching"""
        text_lower = document_text.lower()
        
        # Classification rules
        if any(word in text_lower for word in ['non-disclosure', 'confidential', 'proprietary', 'nda', 'confidentiality']):
            return "Non-Disclosure Agreement (NDA)"
        elif any(word in text_lower for word in ['employment', 'employee', 'job', 'salary', 'work', 'employer']):
            return "Employment Contract"
        elif any(word in text_lower for word in ['service', 'services', 'provide', 'deliver', 'perform']):
            return "Service Agreement"
        elif any(word in text_lower for word in ['lease', 'rent', 'rental', 'tenant', 'landlord', 'premises']):
            return "Lease Agreement"
        elif any(word in text_lower for word in ['purchase', 'buy', 'sale', 'sell', 'buyer', 'seller']):
            return "Purchase Agreement"
        elif any(word in text_lower for word in ['partnership', 'partner', 'joint venture']):
            return "Partnership Agreement"
        elif any(word in text_lower for word in ['license', 'licensing', 'permit', 'intellectual property']):
            return "License Agreement"
        else:
            return "Legal Document"
    
    def extract_obligations(self, text: str) -> List[str]:
        """Extract obligations using pattern matching"""
        obligations = []
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        
        # Obligation keywords
        obligation_patterns = [
            r'\b(shall|must|will|agrees? to|is (?:required|obligated) to|is responsible for)\b',
            r'\b(party|parties|company|employee|contractor)\s+(?:shall|must|will|agrees? to)\b'
        ]
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and len(sentence) < 300:
                for pattern in obligation_patterns:
                    if re.search(pattern, sentence, re.IGNORECASE):
                        obligations.append(sentence.strip() + ".")
                        break
        
        # Return unique obligations, max 5
        unique_obligations = []
        for obligation in obligations:
            if obligation not in unique_obligations and len(unique_obligations) < 5:
                unique_obligations.append(obligation)
        
        return unique_obligations
    
    def generate_summary(self, document_text: str) -> str:
        """Generate a clear, readable summary based on actual document content"""
        if not document_text or len(document_text.strip()) < 20:
            return "The document appears to be too short or empty to generate a meaningful summary."
        
        doc_type = self.classify_document(document_text)
        word_count = len(document_text.split())
        
        # Extract actual content from the document
        parties = self._extract_parties(document_text)
        dates = self._extract_dates(document_text)
        money_amounts = self._extract_money(document_text)
        key_terms = self._extract_key_terms(document_text)
        obligations = self._extract_summary_obligations(document_text)
        
        # Extract key sentences and phrases from the actual document
        key_sentences = self._extract_key_sentences(document_text)
        main_topics = self._identify_main_topics(document_text)
        
        # Build summary based on actual content
        summary_lines = []
        
        # Start with document type and basic info
        summary_lines.append(f"This is a **{doc_type}** containing {word_count:,} words.")
        
        # Add content-based description
        if key_sentences:
            # Use the most important sentence from the document
            main_content = key_sentences[0]
            if len(main_content) > 150:
                main_content = main_content[:150] + "..."
            summary_lines.append(f"The document states: \"{main_content}\"")
        
        # Parties information (only if actually found)
        if parties:
            if len(parties) == 1:
                summary_lines.append(f"The document involves **{parties[0]}**.")
            elif len(parties) == 2:
                summary_lines.append(f"The agreement is between **{parties[0]}** and **{parties[1]}**.")
            else:
                summary_lines.append(f"Multiple parties are involved including **{parties[0]}** and **{parties[1]}**.")
        
        # Main topics covered
        if main_topics:
            if len(main_topics) == 1:
                summary_lines.append(f"The document primarily addresses **{main_topics[0]}**.")
            else:
                summary_lines.append(f"Key topics covered include **{main_topics[0]}** and **{main_topics[1]}**.")
        
        # Financial information (only if found)
        if money_amounts:
            summary_lines.append(f"Financial terms specify amounts of **{money_amounts[0]}**" + 
                               (f" and **{money_amounts[1]}**" if len(money_amounts) > 1 else "") + ".")
        
        # Important dates (only if found)
        if dates:
            summary_lines.append(f"Important dates mentioned include **{dates[0]}**" + 
                               (f" and **{dates[1]}**" if len(dates) > 1 else "") + ".")
        
        # Specific obligations (only if found)
        if obligations:
            clean_obligation = obligations[0].strip()
            if len(clean_obligation) > 100:
                clean_obligation = clean_obligation[:100] + "..."
            summary_lines.append(f"Key obligations include: {clean_obligation}.")
        
        # Add document-specific insights based on actual content
        content_insights = self._generate_content_insights(document_text, doc_type)
        if content_insights:
            summary_lines.append(content_insights)
        
        return " ".join(summary_lines)
    
    def _extract_key_sentences(self, text: str) -> List[str]:
        """Extract the most important sentences from the document"""
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        
        # Filter and rank sentences
        important_sentences = []
        
        # Look for sentences with key legal indicators
        importance_keywords = [
            'agree', 'shall', 'must', 'will', 'party', 'parties', 'contract', 'agreement',
            'obligation', 'responsibility', 'right', 'duty', 'term', 'condition'
        ]
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and len(sentence) < 300:
                # Count importance keywords
                keyword_count = sum(1 for keyword in importance_keywords 
                                  if keyword.lower() in sentence.lower())
                
                if keyword_count > 0:
                    important_sentences.append((sentence, keyword_count))
        
        # Sort by importance and return top sentences
        important_sentences.sort(key=lambda x: x[1], reverse=True)
        return [sent[0] for sent in important_sentences[:3]]
    
    def _identify_main_topics(self, text: str) -> List[str]:
        """Identify main topics discussed in the document"""
        text_lower = text.lower()
        topics = []
        
        topic_keywords = {
            'confidentiality and privacy': ['confidential', 'private', 'secret', 'disclosure'],
            'employment terms': ['employment', 'employee', 'work', 'job', 'salary'],
            'payment and compensation': ['payment', 'pay', 'compensation', 'salary', 'fee'],
            'intellectual property': ['intellectual property', 'copyright', 'trademark', 'patent'],
            'termination conditions': ['terminate', 'termination', 'end', 'expire'],
            'liability and indemnification': ['liable', 'liability', 'indemnify', 'damages'],
            'service delivery': ['service', 'services', 'deliver', 'provide'],
            'property and assets': ['property', 'asset', 'real estate', 'premises'],
            'partnership terms': ['partnership', 'partner', 'joint venture'],
            'licensing rights': ['license', 'licensing', 'permit', 'authorization']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        
        return topics[:3]  # Return top 3 topics
    
    def _generate_content_insights(self, text: str, doc_type: str) -> str:
        """Generate specific insights based on document content"""
        text_lower = text.lower()
        
        # Look for specific content patterns
        if 'confidential' in text_lower and 'information' in text_lower:
            return "The document emphasizes the protection of confidential information and trade secrets."
        
        elif 'employment' in text_lower and ('salary' in text_lower or 'wage' in text_lower):
            return "This employment agreement details compensation and work-related obligations."
        
        elif 'service' in text_lower and ('provide' in text_lower or 'deliver' in text_lower):
            return "The agreement outlines specific services to be provided and delivery expectations."
        
        elif 'lease' in text_lower or 'rent' in text_lower:
            return "This lease agreement establishes rental terms and property usage rights."
        
        elif 'purchase' in text_lower or 'buy' in text_lower or 'sale' in text_lower:
            return "The document facilitates the transfer of ownership for goods or property."
        
        elif 'terminate' in text_lower or 'breach' in text_lower:
            return "The document includes provisions for termination and breach of contract scenarios."
        
        elif 'liability' in text_lower or 'damages' in text_lower:
            return "The agreement addresses liability limitations and damage compensation."
        
        else:
            # Fallback based on document length and complexity
            if len(text.split()) < 100:
                return "This is a brief document outlining basic terms and conditions."
            else:
                return "This comprehensive document establishes detailed legal relationships and obligations."
    
    def _extract_parties(self, text: str) -> List[str]:
        """Extract party names from the document"""
        parties = []
        
        # Look for company names
        company_patterns = [
            r'\b([A-Z][a-zA-Z\s&]+(?:Inc|LLC|Corp|Corporation|Company|Ltd|LLP)\.?)\b',
            r'\b([A-Z][a-zA-Z\s]+(?:Inc|LLC|Corp|Corporation|Company|Ltd|LLP))\b'
        ]
        
        for pattern in company_patterns:
            matches = re.findall(pattern, text)
            parties.extend(matches)
        
        # Look for individual names (basic pattern)
        individual_patterns = [
            r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b(?=\s*(?:,|and|or|\(|$))'
        ]
        
        for pattern in individual_patterns:
            matches = re.findall(pattern, text)
            # Filter out common legal terms that might match
            legal_terms = ['Whereas', 'Therefore', 'Party', 'Agreement', 'Contract']
            matches = [m for m in matches if m not in legal_terms]
            parties.extend(matches[:2])  # Limit individual names
        
        # Remove duplicates and limit
        unique_parties = []
        for party in parties:
            if party not in unique_parties and len(party) > 3:
                unique_parties.append(party)
        
        return unique_parties[:4]  # Max 4 parties
    
    def _extract_dates(self, text: str) -> List[str]:
        """Extract important dates"""
        date_patterns = [
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)
        
        return list(set(dates))[:3]  # Max 3 dates
    
    def _extract_money(self, text: str) -> List[str]:
        """Extract monetary amounts"""
        money_patterns = [
            r'\$[\d,]+(?:\.\d{2})?',
            r'\b\d+(?:,\d{3})*(?:\.\d{2})?\s*dollars?\b',
            r'\bUSD\s*[\d,]+(?:\.\d{2})?\b'
        ]
        
        amounts = []
        for pattern in money_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            amounts.extend(matches)
        
        return list(set(amounts))[:3]  # Max 3 amounts
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key legal terms present in the document"""
        legal_terms = [
            'confidentiality', 'non-disclosure', 'intellectual property', 'copyright',
            'trademark', 'patent', 'liability', 'indemnification', 'termination',
            'breach', 'covenant', 'warranty', 'jurisdiction', 'governing law',
            'force majeure', 'arbitration', 'mediation', 'severability'
        ]
        
        found_terms = []
        text_lower = text.lower()
        
        for term in legal_terms:
            if term in text_lower:
                # Convert to title case for display
                found_terms.append(term.replace('-', ' ').title())
        
        return found_terms[:5]  # Max 5 terms
    
    def _extract_summary_obligations(self, text: str) -> List[str]:
        """Extract main obligations for summary"""
        obligation_patterns = [
            r'(?:shall|must|will|agrees to|required to|responsible for)\s+([^.]{20,100})',
            r'(?:Party|Parties|Company|Employee)\s+(?:shall|must|will|agrees to)\s+([^.]{20,100})'
        ]
        
        obligations = []
        for pattern in obligation_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match.strip()) > 20:
                    obligations.append(match.strip())
        
        return obligations[:3]  # Max 3 obligations
    
    def _determine_purpose(self, text: str, doc_type: str) -> str:
        """Determine the main purpose of the document"""
        text_lower = text.lower()
        
        purpose_indicators = {
            'Non-Disclosure Agreement (NDA)': 'to protect confidential information and trade secrets',
            'Employment Contract': 'to establish terms of employment and work responsibilities',
            'Service Agreement': 'to define services to be provided and payment terms',
            'Lease Agreement': 'to establish rental terms and property usage rights',
            'Purchase Agreement': 'to facilitate the sale and transfer of goods or property',
            'Partnership Agreement': 'to establish business partnership terms and profit sharing',
            'License Agreement': 'to grant usage rights for intellectual property or software'
        }
        
        # Check for specific purpose keywords
        if 'protect' in text_lower and 'confidential' in text_lower:
            return 'to protect confidential information between parties'
        elif 'employment' in text_lower and 'work' in text_lower:
            return 'to establish employment terms and conditions'
        elif 'service' in text_lower and 'provide' in text_lower:
            return 'to outline service delivery and compensation'
        elif 'lease' in text_lower or 'rent' in text_lower:
            return 'to establish property rental terms'
        elif 'purchase' in text_lower or 'sale' in text_lower:
            return 'to facilitate property or asset transfer'
        
        # Fallback to document type purpose
        return purpose_indicators.get(doc_type, 'to establish legal relationships and obligations')
