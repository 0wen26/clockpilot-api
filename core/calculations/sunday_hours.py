# clockpilot/core/calculations/sunday_hours.py
from datetime import datetime, timedelta
from typing import Dict
from core.constants import SUNDAYS, FESTIVOS, MESES_MAP
from core.utils import TimeConverter

def parse_fecha(fecha: str) -> str:
    """Convierte '01-enero' a '01-01' usando MESES_MAP"""
    try:
        dia, mes_nombre = fecha.lower().split("-")
        mes = MESES_MAP.get(mes_nombre)
        return f"{dia}-{mes}" if mes else None
    except:
        return None

def hh_mm_to_timedelta(hhmm: str) -> timedelta:
    try:
        h, m = map(int, hhmm.split(":"))
        return timedelta(hours=h, minutes=m)
    except:
        return timedelta()

def timedelta_to_hh_mm(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours:02}:{minutes:02}"

def calculate_sunday_hours(turnos_por_fecha: Dict[str, dict], year: int) -> str:
    total = timedelta()
    domingos = SUNDAYS.get(year, set())

    for fecha, datos in turnos_por_fecha.items():
        fecha_formateada = parse_fecha(fecha)
        if fecha_formateada in domingos:
            duracion = datos.get("duracion_total", "00:00")
            if isinstance(duracion, timedelta):
                total += duracion
            else:
                total += hh_mm_to_timedelta(duracion)

    return timedelta_to_hh_mm(total)

def calculate_festive_hours(turnos_por_fecha: Dict[str, dict], year: int) -> str:
    total = timedelta()
    festivos = FESTIVOS.get(year, set())
    domingos = SUNDAYS.get(year, set())

    for fecha, datos in turnos_por_fecha.items():
        fecha_formateada = parse_fecha(fecha)
        if fecha_formateada in festivos and fecha_formateada not in domingos:
            duracion = datos.get("duracion_total", "00:00")
            if isinstance(duracion, timedelta):
                total += duracion
            else:
                total += hh_mm_to_timedelta(duracion)

    return timedelta_to_hh_mm(total)
