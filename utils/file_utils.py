#clockpilot/utils/file_utils.py
import os

def validate_file_path(file_path):
    """Valida que la ruta del archivo sea válida."""
    if not file_path:
        return "Por favor selecciona un archivo."
    if not os.path.exists(file_path):
        return "El archivo seleccionado no existe."
    return None

def cleanup_temp_files():
    """Elimina archivos temporales generados por la aplicación."""
    pass  # Implementar lógica para eliminar archivos temporales si es necesario