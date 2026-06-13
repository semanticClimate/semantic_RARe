import os
import pdfplumber

def parse_pdf_by_page(file_path: str) -> list[str]:
    """
    Extracts text page-by-page from a PDF, preserving layout.
    Filters out blank or irrelevant short pages.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find PDF at: {file_path}")
        
    pages_data = []
    
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text(layout=True)
            # Only keep pages with substantial content (>50 characters)
            if text and len(text.strip()) > 50:
                pages_data.append(text)
                
    return pages_data