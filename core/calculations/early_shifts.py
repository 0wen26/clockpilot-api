# clockpilot/core/calculations/early_shifts.py
from datetime import datetime, time
from typing import Dict, List

FMT = "%H:%M"
INICIO = time(4, 0)
FIN = time(6, 55)


def calculate_madrugue_hours(turnos_por_fecha: Dict[str, dict]) -> str:
    """
    Cuenta los días con al menos un turno que comienza entre las 04:00 y 06:55.

    Args:
        turnos_por_fecha: Diccionario {fecha: {turnos: [turno1, turno2, ...]}}

    Returns:
        Total de días con madrugue, en formato "XX" (2 dígitos).
    """
    total = 0

    for datos in turnos_por_fecha.values():
        for turno in datos.get("turnos", []):
            try:
                hora = datetime.strptime(turno["hora_entrada"], FMT).time()
                if INICIO <= hora <= FIN:
                    total += 1
                    break  # Solo una vez por día
            except (KeyError, ValueError):
                continue

    return f"{total:02d}"
