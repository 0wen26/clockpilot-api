# services/data_io.py
import json
import os
from core.constants import OUTPUT_JSON

def save_to_json(data, file_path="assets/output.json"):
    """Guarda los datos en un archivo JSON."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_from_json(file_path="assets/output.json"):
    """Carga los datos desde un archivo JSON."""
    if not os.path.exists(file_path):
        return {}  # Devuelve un JSON vacío sin mostrar advertencia
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def delete_json(file_path="assets/output.json"):
    """Elimina el archivo JSON si existe."""
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Archivo {file_path} eliminado.")
    else:
        print(f"El archivo {file_path} no existe.")

def json_exists():
    """Verifica si el archivo JSON existe."""
    return os.path.exists(OUTPUT_JSON)