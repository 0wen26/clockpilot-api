# clockpilot/core/calculations/complementary_hours.py
from typing import Union


def calculate_complementary_hours(horas_contrato: int, total_hours: str, perentorias: str) -> str:
    """
    Calcula las horas complementarias:
    Horas Complementarias = Total - (Contrato + Perentorias)

    Args:
        horas_contrato: Horas de contrato en entero (ej. 84)
        total_hours: Total trabajado, formato HH:MM
        perentorias: Horas HR, formato HH:MM

    Returns:
        Resultado en formato HH:MM
    """
    try:
        total_min = _hhmm_to_minutos(total_hours)
        perentorias_min = _hhmm_to_minutos(perentorias)
        contrato_min = horas_contrato * 60

        restantes = max(0, total_min - (contrato_min + perentorias_min))
        return _minutos_to_hhmm(restantes)
    except:
        return "00:00"


def _hhmm_to_minutos(hhmm: Union[str, None]) -> int:
    try:
        h, m = map(int, hhmm.split(":"))
        return h * 60 + m
    except:
        return 0


def _minutos_to_hhmm(minutos: int) -> str:
    h = minutos // 60
    m = minutos % 60
    return f"{h:02}:{m:02}"