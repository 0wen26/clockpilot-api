# clockpilot/core/file_processing/models.py
from datetime import datetime, timedelta, date
from typing import Dict, List, TypedDict, Optional

class Shift(TypedDict):
    hora_entrada: str
    hora_salida: str
    tipo: str  # 'HR' o 'Normal'

class DailyData(TypedDict):
    turnos: List[Shift]
    duracion_total: timedelta
    horas_perentorias: timedelta
    festive_hours: str
    horas_domingos: str
    dias_madrugue: int
    horas_nocturnas: str
    viandas_comida: int
    turnos_fraccionados: int
    fecha_obj: Optional[date]

class ProcessedPDFData(TypedDict):
    shifts_by_date: Dict[str, DailyData]
    totals: Dict[str, str]