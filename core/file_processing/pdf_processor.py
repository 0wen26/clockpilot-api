# clockpilot/core/file_processing/pdf_processor.py
import re
from datetime import timedelta, datetime
from typing import Dict
from PyPDF2 import PdfReader
from core.utils import TimeConverter, DateProcessor
from core.calculations import (
    calculate_festive_hours,
    calculate_sunday_hours,
    calculate_madrugue_hours,
    calculate_meal_allowance,
    calculate_split_shift,
    calculate_night_hours,
    calculate_complementary_hours,
)
from core.file_processing.models import DailyData, ProcessedPDFData


fecha_pattern = re.compile(r'\d{2}-[A-Za-z]+')
hora_pattern = re.compile(r'\b\d{2}:\d{2}')
duracion_pattern = re.compile(r'\b\d{1,2}:\d{2}\b$')

meses_abreviados = {
    "Ene": "Enero", "Feb": "Febrero", "Mar": "Marzo", "Abr": "Abril",
    "May": "Mayo", "Jun": "Junio", "Jul": "Julio", "Ago": "Agosto",
    "Sep": "Septiembre", "Oct": "Octubre", "Nov": "Noviembre",
    "D?mbre": "Diciembre", "D": "Diciembre"
}


class PDFProcessor:
    def __init__(self, year: int):
        self.year = year
        self.time = TimeConverter()

    def process_pdf(self, pdf_path: str, contract_hours: int) -> ProcessedPDFData:
        text = self._extract_text_from_pdf(pdf_path)
        lines = text.splitlines()

        turnos_por_fecha: Dict[str, DailyData] = {}
        current_date = None

        for line in lines:
            fecha_match = fecha_pattern.search(line)
            if fecha_match:
                fecha_abreviada = fecha_match.group()
                dia, mes_abreviado = fecha_abreviada.split('-')
                mes_completo = meses_abreviados.get(mes_abreviado, mes_abreviado)
                current_date = f"{dia}-{mes_completo}"
                if current_date not in turnos_por_fecha:
                    turnos_por_fecha[current_date] = {
                        "turnos": [],
                        "duracion_total": timedelta(),
                        "horas_perentorias": timedelta(),
                    }

            if current_date:
                self._process_line(line, current_date, turnos_por_fecha)

        # Cálculos por día
        for fecha, datos in turnos_por_fecha.items():
            datos["festive_hours"] = calculate_festive_hours({fecha: datos}, self.year)
            datos["horas_domingos"] = calculate_sunday_hours({fecha: datos}, self.year)
            datos["dias_madrugue"] = int(calculate_madrugue_hours({fecha: datos}))
            datos["horas_nocturnas"] = calculate_night_hours({fecha: datos})
            datos["viandas_comida"] = calculate_meal_allowance({fecha: datos})
            datos["turnos_fraccionados"] = calculate_split_shift({fecha: datos})

        # Cálculos totales
        totals = {
            "total_hours": self._sum_metric(turnos_por_fecha, "duracion_total"),
            "total_hr_hours": self._sum_metric(turnos_por_fecha, "horas_perentorias"),
            "complementary_hours": calculate_complementary_hours(
                contract_hours,
                self._sum_metric(turnos_por_fecha, "duracion_total"),
                self._sum_metric(turnos_por_fecha, "horas_perentorias")
            ),
            "total_festive_hours": calculate_festive_hours(turnos_por_fecha, self.year),
            "total_sunday_hours": calculate_sunday_hours(turnos_por_fecha, self.year),
            "total_early_days": calculate_madrugue_hours(turnos_por_fecha),
            "total_night_hours": calculate_night_hours(turnos_por_fecha),
            "total_meal_allowance": calculate_meal_allowance(turnos_por_fecha),
            "total_split_shifts": calculate_split_shift(turnos_por_fecha),
        }

        return {
            "shifts_by_date": turnos_por_fecha,
            "totals": totals
        }

    def _process_line(self, line: str, current_date: str, target: Dict[str, DailyData]):
        palabras = line.split()
        horas = []
        duracion_match = duracion_pattern.search(line)
        duracion = duracion_match.group() if duracion_match else None

        hay_hr_en_linea = "HR" in line.upper()

        i = 0
        while i < len(palabras):
            if hora_pattern.match(palabras[i]):
                if i > 0 and palabras[i - 1].lower() == "bcn":
                    i += 2
                    continue
                if i + 1 < len(palabras) and hora_pattern.match(palabras[i + 1]):
                    entrada, salida = palabras[i], palabras[i + 1]
                    tipo = "HR" if hay_hr_en_linea else "Normal"
                    horas.append((entrada, salida, tipo, duracion))
                    i += 2
                else:
                    i += 1
            else:
                i += 1

        for entrada, salida, tipo, duracion in horas:
            turno = {"hora_entrada": entrada, "hora_salida": salida, "tipo": tipo}
            if turno not in target[current_date]["turnos"]:
                duracion_td = self.time.calculate_shift_duration(entrada, salida)
                target[current_date]["turnos"].append(turno)
                target[current_date]["duracion_total"] += duracion_td
                if tipo == "HR":
                    target[current_date]["horas_perentorias"] += duracion_td

    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        try:
            with open(pdf_path, 'rb') as f:
                reader = PdfReader(f)
                return "\n".join([page.extract_text() or "" for page in reader.pages])
        except Exception as e:
            print(f"Error al leer el PDF: {e}")
            return ""

    def _sum_metric(self, data: Dict[str, DailyData], key: str) -> str:
        total = timedelta()
        for dia in data.values():
            valor = dia.get(key, timedelta())
            if isinstance(valor, str):
                valor = self.time.hh_mm_to_timedelta(valor)
            total += valor
        return self.time.timedelta_to_hh_mm(total)