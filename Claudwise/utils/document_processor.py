"""
Document processing utilities for multiple file formats
"""

import PyPDF2
from docx import Document
import io
from typing import Optional, List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Process documents in various formats (PDF, DOCX, TXT)"""
    
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise Exception(f"Failed to process PDF: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(file_content: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(io.BytesIO(file_content))
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {e}")
            raise Exception(f"Failed to process DOCX: {str(e)}")
    
    @staticmethod
    def extract_text_from_txt(file_content: bytes) -> str:
        """Extract text from TXT file"""
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    text = file_content.decode(encoding)
                    return text.strip()
                except UnicodeDecodeError:
                    continue
            
            # If all encodings fail, use utf-8 with error handling
            text = file_content.decode('utf-8', errors='ignore')
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from TXT: {e}")
            raise Exception(f"Failed to process TXT: {str(e)}")
    
    @staticmethod
    def process_document(file_content: bytes, file_type: str) -> str:
        """Process document based on file type"""
        file_type = file_type.lower()
        
        if file_type == '.pdf':
            return DocumentProcessor.extract_text_from_pdf(file_content)
        elif file_type == '.docx':
            return DocumentProcessor.extract_text_from_docx(file_content)
        elif file_type == '.txt':
            return DocumentProcessor.extract_text_from_txt(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    @staticmethod
    def validate_file_size(file_size: int, max_size: int = 10 * 1024 * 1024) -> bool:
        """Validate file size (default max: 10MB)"""
        return file_size <= max_size
    
    @staticmethod
    def get_file_info(file_content: bytes, filename: str) -> Dict:
        """Get basic file information"""
        return {
            'filename': filename,
            'size_bytes': len(file_content),
            'size_mb': round(len(file_content) / (1024 * 1024), 2),
            'file_type': filename.split('.')[-1].lower() if '.' in filename else 'unknown'
        }
