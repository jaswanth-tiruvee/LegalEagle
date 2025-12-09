"""
PDF processing module for extracting and chunking text from legal contracts.
"""
import PyPDF2
from typing import List, Tuple
from langchain_text_splitters import RecursiveCharacterTextSplitter
import config


class PDFProcessor:
    """Handles PDF extraction and text chunking with page tracking."""
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or config.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or config.CHUNK_OVERLAP
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
        )
    
    def extract_text_from_pdf(self, pdf_path: str) -> List[Tuple[str, int]]:
        """
        Extract text from PDF with page number tracking.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of tuples (text, page_number)
        """
        text_with_pages = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                for page_num in range(total_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    
                    if text.strip():  # Only add non-empty pages
                        text_with_pages.append((text, page_num + 1))
        
        except Exception as e:
            raise Exception(f"Error reading PDF {pdf_path}: {str(e)}")
        
        return text_with_pages
    
    def chunk_text(self, text_with_pages: List[Tuple[str, int]]) -> List[dict]:
        """
        Chunk text while preserving page number information.
        
        Args:
            text_with_pages: List of (text, page_number) tuples
            
        Returns:
            List of dictionaries with 'text', 'page', and 'metadata' keys
        """
        chunks = []
        
        for text, page_num in text_with_pages:
            # Split text into chunks
            text_chunks = self.text_splitter.split_text(text)
            
            for chunk in text_chunks:
                chunks.append({
                    'text': chunk,
                    'page': page_num,
                    'metadata': {
                        'source': 'contract',
                        'page': page_num,
                        'chunk_length': len(chunk)
                    }
                })
        
        return chunks

