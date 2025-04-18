# services/pdf/pdf_extractor.py
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):
    """Extrae todo el texto de un archivo PDF."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            return "".join([page.extract_text() + "\n" for page in reader.pages])
    except Exception as e:
        print(f"Error al leer el PDF: {e}")
        return ""