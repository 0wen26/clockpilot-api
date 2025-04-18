# clockpilot/core/calculations/meal_allowance.py
from datetime import datetime, timedelta
from typing import Dict, List

FMT = "%H:%M"
MIN_DURATION = timedelta(hours=6)


def calculate_meal_allowance(turnos_por_fecha: Dict[str, dict]) -> int:
    """
    Calcula cuántos días tienen derecho a manutención por cubrir franjas horarias
    con un turno de al menos 6 horas que incluya almuerzo (14-16) o cena (21-23).
    
    Args:
        turnos_por_fecha: Diccionario {fecha: {turnos: [turno1, turno2, ...]}}

    Returns:
        Total de días con derecho a vianda.
    """
    total = 0

    for fecha, datos in turnos_por_fecha.items():
        turnos_dia = [t for t in datos.get("turnos", [])
                      if t["hora_entrada"] != "00:00" or t["hora_salida"] != "00:00"]

        if not turnos_dia:
            continue

        # Obtener turno principal (más largo)
        turno_principal = max(
            turnos_dia,
            key=lambda t: _duracion_turno(t["hora_entrada"], t["hora_salida"]),
        )

        entrada = datetime.strptime(turno_principal["hora_entrada"], FMT)
        salida = datetime.strptime(turno_principal["hora_salida"], FMT)
        if salida <= entrada:
            salida += timedelta(days=1)

        # Expandir con turnos adyacentes conectados
        for turno in turnos_dia:
            if turno == turno_principal:
                continue
            entrada_aux = datetime.strptime(turno["hora_entrada"], FMT)
            salida_aux = datetime.strptime(turno["hora_salida"], FMT)
            if salida_aux <= entrada_aux:
                salida_aux += timedelta(days=1)

            if entrada_aux == salida:
                salida = salida_aux
            elif salida_aux == entrada:
                entrada = entrada_aux

        duracion = salida - entrada
        if duracion < MIN_DURATION:
            continue

        # Comprobar franjas horarias
        if _incluye_franja(entrada, salida, 14, 16) or _incluye_franja(entrada, salida, 21, 23):
            total += 1

    return total


def _duracion_turno(hora_inicio: str, hora_fin: str) -> timedelta:
    try:
        entrada = datetime.strptime(hora_inicio, FMT)
        salida = datetime.strptime(hora_fin, FMT)
        if salida <= entrada:
            salida += timedelta(days=1)
        return salida - entrada
    except ValueError:
        return timedelta()


def _incluye_franja(entrada: datetime, salida: datetime, hora_inicio: int, hora_fin: int) -> bool:
    inicio_franja = entrada.replace(hour=hora_inicio, minute=0)
    fin_franja = entrada.replace(hour=hora_fin, minute=0)
    return entrada <= inicio_franja and salida >= fin_franja
