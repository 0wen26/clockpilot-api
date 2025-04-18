# clockpilot/core/calculations/split_shifts.py
from datetime import datetime, timedelta
from typing import Dict

FMT = "%H:%M"
MIN_GAP = timedelta(hours=1)
MAX_GAP = timedelta(hours=5)


def calculate_split_shift(turnos_por_fecha: Dict[str, dict]) -> int:
    """
    Calcula el número de días con turnos fraccionados (mínimo 2 turnos separados entre 1h y 5h).

    Args:
        turnos_por_fecha: Diccionario {fecha: {turnos: [turno1, turno2, ...]}}

    Returns:
        Total de días con jornada fraccionada.
    """
    total = 0

    for fecha, datos in turnos_por_fecha.items():
        turnos = [t for t in datos.get("turnos", []) if t["hora_entrada"] != "00:00" or t["hora_salida"] != "00:00"]
        if len(turnos) < 2:
            continue

        turnos.sort(key=lambda t: datetime.strptime(t["hora_entrada"], FMT))

        for i in range(len(turnos) - 1):
            salida_actual = datetime.strptime(turnos[i]["hora_salida"], FMT)
            entrada_siguiente = datetime.strptime(turnos[i + 1]["hora_entrada"], FMT)

            if salida_actual <= datetime.strptime(turnos[i]["hora_entrada"], FMT):
                salida_actual += timedelta(days=1)

            if entrada_siguiente <= salida_actual:
                entrada_siguiente += timedelta(days=1)

            diferencia = entrada_siguiente - salida_actual
            if MIN_GAP <= diferencia <= MAX_GAP:
                total += 1
                break  # Solo una vez por día

    return total
