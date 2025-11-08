"""
Configuration file for ClauseWise application
"""

# Model Configuration
GRANITE_MODEL = "ibm-granite/granite-3.2-2b-instruct"
SPACY_MODEL = "en_core_web_sm"

# Document Processing
SUPPORTED_FORMATS = ['.pdf', '.docx', '.txt']
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Legal Document Types
DOCUMENT_TYPES = [
    "Non-Disclosure Agreement (NDA)",
    "Employment Contract", 
    "Service Agreement",
    "Lease Agreement",
    "Purchase Agreement",
    "Partnership Agreement",
    "License Agreement",
    "Other"
]

# Legal Entities for NER
LEGAL_ENTITIES = [
    "PARTY",
    "DATE", 
    "MONEY",
    "OBLIGATION",
    "TERM",
    "JURISDICTION",
    "PENALTY"
]

# Streamlit Configuration
PAGE_TITLE = "ClauseWise - AI Legal Document Analyzer"
PAGE_ICON = "⚖️"
LAYOUT = "wide"
