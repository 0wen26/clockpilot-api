# clockpilot/core/validators.py

def validate_pdf_path(pdf_path: str) -> str | None:
    """Valida que la ruta del PDF sea válida."""
    if not pdf_path:
        return "Por favor selecciona un archivo PDF."
    if not pdf_path.lower().endswith(".pdf"):
        return "El archivo seleccionado no es un PDF válido."
    return None

def validate_contract_hours(hours: str) -> str | None:
    """Valida que las horas de contrato sean un número válido."""
    if not hours.isdigit():
        return "Por favor ingresa un número válido para las horas de contrato."
    return None