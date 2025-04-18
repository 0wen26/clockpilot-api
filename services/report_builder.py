# services/report_builder.py
import json
from core.models import DaySummary
from core.utils import sum_times, hh_mm_to_decimal

def build_report(turnos_por_fecha, horas_contrato, year):
    """Construye el informe completo a partir de los datos procesados."""
    totales = {
        "total_hours": sum_times(datos["duracion_total"] for datos in turnos_por_fecha.values()),
        "total_hr_hours": sum_times(datos["horas_perentorias"] for datos in turnos_por_fecha.values()),
        "total_festive_hours": sum_times(datos["festive_hours"] for datos in turnos_por_fecha.values()),
        "total_sundays_hours": sum_times(datos["horas_domingos"] for datos in turnos_por_fecha.values()),
        "total_madrugue_days": sum_times(datos["horas_madrugue"] for datos in turnos_por_fecha.values()),
        "total_night_hours": sum_times(datos["horas_nocturnas"] for datos in turnos_por_fecha.values()),
        "total_meal_allowance": sum(datos["manutencion"] for datos in turnos_por_fecha.values()),
        "total_split_shifts": sum(datos["fraccionadas"] for datos in turnos_por_fecha.values())
    }

    # Convertir los totales a formato decimal
    totales["total_hours_decimal"] = hh_mm_to_decimal(totales["total_hours"])
    totales["total_hr_hours_decimal"] = hh_mm_to_decimal(totales["total_hr_hours"])
    totales["total_festive_hours_decimal"] = hh_mm_to_decimal(totales["total_festive_hours"])
    totales["total_sundays_hours_decimal"] = hh_mm_to_decimal(totales["total_sundays_hours"])
    totales["total_night_hours_decimal"] = hh_mm_to_decimal(totales["total_night_hours"])

    # Crear el diccionario final con "detalles" y "totales"
    final_data = {
        "detalles": turnos_por_fecha,
        "totales": totales,
        "horas_contrato": horas_contrato,
        "year": year
    }

    return final_data