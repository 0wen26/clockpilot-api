#clockpilot/utils/time_tools.py
from datetime import timedelta

def timedelta_to_hh_mm(td):
    """Convierte un timedelta a formato HH:MM."""
    total_horas = int(td.total_seconds() // 3600)
    total_minutos = int((td.total_seconds() % 3600) // 60)
    return f"{total_horas:02}:{total_minutos:02}"

def hh_mm_to_timedelta(time_str):
    """Convierte una cadena 'HH:MM' a un objeto timedelta."""
    try:
        hours, minutes = map(int, time_str.split(":"))
        return timedelta(hours=hours, minutes=minutes)
    except (ValueError, AttributeError):
        return timedelta()  # Devuelve 0 si hay un error

def sum_times(times):
    """Suma una lista de tiempos en formato 'HH:MM'."""
    total_td = timedelta()
    for t in list(times):  # Convertir el generador en una lista
        if isinstance(t, str):  # Solo procesar si es una cadena
            hours, minutes = map(int, t.split(':'))
            total_td += timedelta(hours=hours, minutes=minutes)
        elif isinstance(t, int):  # Si es un entero, conviértelo a HH:MM
            total_td += timedelta(hours=t)
    hours = int(total_td.total_seconds() // 3600)
    minutes = int((total_td.total_seconds() % 3600) // 60)
    return f"{hours:02}:{minutes:02}"

def hh_mm_to_decimal(time_str):
    """
    Convierte una cadena 'HH:MM' a un número decimal con 2 decimales.
    Ejemplo: "03:30" -> 3.50
    """
    try:
        hours, minutes = map(int, time_str.split(":"))
        return round(hours + (minutes / 60), 2)  # Redondear a 2 decimales
    except (ValueError, AttributeError):
        return 0.00  # Devuelve 0 si hay un error