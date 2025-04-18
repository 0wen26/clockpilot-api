# core/calculations/festive_hours.py
from datetime import datetime, timedelta
from typing import Dict
from core.constants import FESTIVOS, MESES_MAP
from core.utils import DateProcessor

def parse_fecha(fecha: str) -> str:
    """Convierte '01-enero' a '01-01' usando MESES_MAP"""
    try:
        dia, mes_nombre = fecha.lower().split("-")
        mes = MESES_MAP.get(mes_nombre)
        return f"{dia}-{mes}" if mes else None
    except:
        return None

def _hh_mm_to_timedelta(time_str: str) -> timedelta:
    try:
        h, m = map(int, time_str.split(":"))
        return timedelta(hours=h, minutes=m)
    except:
        return timedelta()

def _timedelta_to_hh_mm(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours:02}:{minutes:02}"

def _es_festivo_valido(fecha_str: str, festivos: set, domingos: set) -> bool:
    return fecha_str in festivos and fecha_str not in domingos

def calculate_festive_hours(turnos_por_fecha: Dict[str, dict], year: int) -> str:
    """
    Calcula las horas trabajadas en festivos (que NO sean domingo).

    Args:
        turnos_por_fecha: Diccionario {fecha: {...}}
        year: Año a considerar

    Returns:
        Total de horas en festivos en formato HH:MM
    """
    from core.constants import SUNDAYS  # Importar aquí para evitar errores de dependencia cruzada

    total = timedelta()
    festivos = FESTIVOS.get(year, set())
    domingos = SUNDAYS.get(year, set())

    for fecha_str, datos in turnos_por_fecha.items():
        fecha_formateada = parse_fecha(fecha_str)
        if not fecha_formateada:
            continue

        if _es_festivo_valido(fecha_formateada, festivos, domingos):
            duracion = datos.get("duracion_total", "00:00")
            if isinstance(duracion, timedelta):
                total += duracion
            else:
                total += _hh_mm_to_timedelta(duracion)

    return _timedelta_to_hh_mm(total)