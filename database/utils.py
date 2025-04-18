# clockpilot/database/utils.py

from core.constants import MESES_MAP_INV
from datetime import datetime

def convertir_claves_a_dd_mes(diccionario):
    """
    Convierte claves YYYY-MM-DD a formato dd-MMMM (ej: 01-Mayo).
    """
    nuevo_diccionario = {}
    for clave in diccionario:
        try:
            fecha_obj = datetime.strptime(clave, "%Y-%m-%d")
            nombre_mes = MESES_MAP_INV[fecha_obj.month]
            nueva_clave = f"{fecha_obj.day:02d}-{nombre_mes}"
            nuevo_diccionario[nueva_clave] = diccionario[clave]
        except Exception as e:
            print(f"❌ Error al convertir clave '{clave}': {e}")
    return nuevo_diccionario

def hh_mm_to_decimal(time_str):
    """
    Convierte una cadena 'HH:MM' a decimal. Ej: "03:30" -> 3.50
    """
    try:
        hours, minutes = map(int, time_str.split(":"))
        return round(hours + (minutes / 60), 2)
    except (ValueError, AttributeError):
        return 0.00
