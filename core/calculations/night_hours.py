# clockpilot/core/calculations/night_hours.py
from datetime import datetime, timedelta
from typing import Dict

FMT = "%H:%M"


def calculate_night_hours(turnos_por_fecha: Dict[str, dict]) -> str:
    """
    Calcula las horas trabajadas entre las 22:00 y 06:00.

    Args:
        turnos_por_fecha: Diccionario {fecha: {turnos: [turno1, turno2, ...]}}

    Returns:
        Total de horas nocturnas en formato HH:MM
    """
    total = timedelta()

    for fecha, datos in turnos_por_fecha.items():
        for turno in datos.get("turnos", []):
            entrada = turno.get("hora_entrada")
            salida = turno.get("hora_salida")

            if entrada == "00:00" and salida == "00:00":
                continue  # vacaciones

            try:
                entrada_dt = datetime.strptime(entrada, FMT)
                salida_dt = datetime.strptime(salida, FMT)
                if salida_dt <= entrada_dt:
                    salida_dt += timedelta(days=1)

                # Rango nocturno (22:00 a 06:00)
                noche_inicio = entrada_dt.replace(hour=22, minute=0)
                if entrada_dt.hour < 6:
                    noche_inicio -= timedelta(days=1)
                noche_fin = noche_inicio + timedelta(hours=8)

                inicio_nocturno = max(entrada_dt, noche_inicio)
                fin_nocturno = min(salida_dt, noche_fin)

                if inicio_nocturno < fin_nocturno:
                    total += fin_nocturno - inicio_nocturno

            except ValueError:
                continue

    return _timedelta_to_hh_mm(total)


def _timedelta_to_hh_mm(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours:02}:{minutes:02}"
