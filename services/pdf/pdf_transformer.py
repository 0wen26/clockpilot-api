# services/pdf/pdf_transformer.py
import re
import json
from datetime import timedelta, datetime
from pypdf import PdfReader
from core.constants import OUTPUT_JSON, meses_abreviados
from core.utils import sum_times, hh_mm_to_decimal, hh_mm_to_timedelta
from core.calculations.festive_hours import calculate_festive_hours
from core.calculations.sunday_hours import calculate_sunday_hours
from core.calculations.early_shifts import calculate_madrugue_hours
from core.calculations.meal_allowance import calculate_meal_allowance
from core.calculations.split_shifts import calculate_split_shift
from core.calculations.night_hours import calculate_night_hours
from services.pdf.pdf_extractor import extract_text_from_pdf

# Expresiones regulares para fechas, horas y duraciones
fecha_pattern = re.compile(r'\d{2}-[A-Za-z]+')  # Captura solo el número del día y el mes
hora_pattern = re.compile(r'\b\d{2}:\d{2}')
duracion_pattern = re.compile(r'\b\d{1,2}:\d{2}\b$')

def process_line(line, current_date, turnos_por_fecha):
    """Procesa una línea de texto del PDF para extraer turnos y horas."""
    palabras = line.split()
    horas = []
    tiene_hr = "HR" in line
    duracion_match = duracion_pattern.search(line)
    duracion = duracion_match.group() if duracion_match else None

    i = 0
    while i < len(palabras):
        if hora_pattern.match(palabras[i]):
            if i > 0 and palabras[i - 1].lower() == "bcn":
                i += 2
                continue
            if i + 1 < len(palabras) and hora_pattern.match(palabras[i + 1]):
                entrada, salida = palabras[i], palabras[i + 1]
                horas.append((entrada, salida, tiene_hr, duracion))
                i += 2
            else:
                i += 1
        else:
            i += 1

    for entrada, salida, es_hr, duracion in horas:
        turno = {"hora_entrada": entrada, "hora_salida": salida}
        if es_hr:
            turno["tipo"] = "HR"
        if duracion:
            duracion_td = timedelta(hours=int(duracion.split(':')[0]), minutes=int(duracion.split(':')[1]))
            turnos_por_fecha[current_date]["duracion_total"] += duracion_td
        turnos_por_fecha[current_date]["turnos"].append(turno)

def parse_pdf_to_json(pdf_path, output_json=None, year=2024, horas_contrato=84):
    """Procesa el PDF y guarda la información de turnos en un JSON, desglosando cada día correctamente."""
    turnos_por_fecha = {}
    text = extract_text_from_pdf(pdf_path)
    lines = text.splitlines()
    current_date = None

    total_duration = timedelta()
    total_hr_duration = timedelta()

    for line in lines:
        fecha_match = fecha_pattern.search(line)
        if fecha_match:
            fecha_abreviada = fecha_match.group()
            # Extraer el número del día y el mes
            dia, mes_abreviado = fecha_abreviada.split('-')
            # Convertir el mes abreviado a su nombre completo usando el diccionario
            mes_completo = meses_abreviados.get(mes_abreviado, mes_abreviado)
            # Reconstruir la fecha con el número del día y el mes completo
            current_date = f"{dia}-{mes_completo}"
            if current_date not in turnos_por_fecha:
                turnos_por_fecha[current_date] = {
                    "turnos": [],
                    "duracion_total": timedelta(),
                    "horas_perentorias": timedelta(),
                    "festive_hours": timedelta(),
                    "horas_domingos": timedelta(),
                    "horas_madrugue": timedelta(),
                    "horas_nocturnas": timedelta(),
                    "manutencion": 0,
                    "fraccionadas": 0,
                }

        if current_date:
            process_line(line, current_date, turnos_por_fecha)

    # Calcular todas las métricas para cada día
    for fecha, datos in turnos_por_fecha.items():
        duracion_total = datos["duracion_total"]
        datos["duracion_total"] = f"{int(duracion_total.total_seconds() // 3600):02}:{int((duracion_total.total_seconds() % 3600) // 60):02}"

        total_duration += duracion_total

        # Calcular horas HR (perentorias) para cada día
        horas_perentorias = timedelta()
        for turno in datos["turnos"]:
            if "tipo" in turno and turno["tipo"] == "HR":
                entrada = turno["hora_entrada"]
                salida = turno["hora_salida"]
                fmt = "%H:%M"
                entrada_time = datetime.strptime(entrada, fmt)
                salida_time = datetime.strptime(salida, fmt)

                if salida_time < entrada_time:
                    salida_time += timedelta(days=1)

                hr_duracion = salida_time - entrada_time
                horas_perentorias += hr_duracion
                total_hr_duration += hr_duracion

        datos["horas_perentorias"] = f"{int(horas_perentorias.total_seconds() // 3600):02}:{int((horas_perentorias.total_seconds() % 3600) // 60):02}"

        # Calcular las métricas individuales por fecha
        datos["festive_hours"] = calculate_festive_hours({fecha: datos}, year)
        datos["horas_domingos"] = calculate_sunday_hours({fecha: datos}, year)
        datos["horas_madrugue"] = calculate_madrugue_hours({fecha: datos})
        datos["manutencion"] = calculate_meal_allowance({fecha: datos})
        datos["fraccionadas"] = calculate_split_shift({fecha: datos})
        datos["horas_nocturnas"] = calculate_night_hours({fecha: datos})

    # Crear el diccionario final con "detalles" y "totales"
    final_data = {
        "detalles": turnos_por_fecha,
        "totales": {
            "total_hours": sum_times(datos["duracion_total"] for datos in turnos_por_fecha.values()),
            "total_hr_hours": sum_times(datos["horas_perentorias"] for datos in turnos_por_fecha.values()),
            "total_festive_hours": sum_times(datos["festive_hours"] for datos in turnos_por_fecha.values()),
            "total_sundays_hours": sum_times(datos["horas_domingos"] for datos in turnos_por_fecha.values()),
            "total_madrugue_days": sum_times(datos["horas_madrugue"] for datos in turnos_por_fecha.values()),
            "total_night_hours": sum_times(datos["horas_nocturnas"] for datos in turnos_por_fecha.values()),
            "total_meal_allowance": sum(datos["manutencion"] for datos in turnos_por_fecha.values()),
            "total_split_shifts": sum(datos["fraccionadas"] for datos in turnos_por_fecha.values())
        },
        "horas_contrato": horas_contrato,  # Añadir horas de contrato
        "year": year  # Añadir el año
    }

    # Convertir los totales a formato decimal
    final_data["totales"]["total_hours_decimal"] = hh_mm_to_decimal(final_data["totales"]["total_hours"])
    final_data["totales"]["total_hr_hours_decimal"] = hh_mm_to_decimal(final_data["totales"]["total_hr_hours"])
    final_data["totales"]["total_festive_hours_decimal"] = hh_mm_to_decimal(final_data["totales"]["total_festive_hours"])
    final_data["totales"]["total_sundays_hours_decimal"] = hh_mm_to_decimal(final_data["totales"]["total_sundays_hours"])
    final_data["totales"]["total_night_hours_decimal"] = hh_mm_to_decimal(final_data["totales"]["total_night_hours"])

    # Si no se proporciona una ruta de salida, usar la ruta definida en constants.py
    if output_json is None:
        output_json = OUTPUT_JSON

    # Guardar el JSON
    with open(output_json, 'w') as f:
        json.dump(final_data, f, indent=4, ensure_ascii=False)

    print(f"Archivo JSON guardado en: {output_json}")
    return output_json