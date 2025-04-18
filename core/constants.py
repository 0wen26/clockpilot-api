# clockpilot/core/constants.py

import os
import sys

# Detectar si se ejecuta como .exe (PyInstaller)
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images")
OUTPUT_JSON = os.path.join(os.path.dirname(sys.executable), "output.json")

CARD_COLORS = {
    "Horas Contrato": "#FFB6C1",
    "Total Horas": "#ADD8E6",
    "Horas Complementarias": "#90EE90",
    "Horas Perentorias": "#FFD700",
    "Horas Festivas": "#FFA500",
    "Horas Domingos": "#FF4500",
    "Horas Nocturnas": "#6A5ACD",
    "Madrugues": "#20B2AA",
    "Manutención": "#D2691E",
    "Fraccionadas": "#8B4513",
}

DATA = [
    ("Horas Contrato", 160, "contract.jpg"),
    ("Total Horas", "--:--", "clock.jpg"),
    ("Horas Complementarias", "--:--", "plus.jpg"),
    ("Horas Perentorias", "--:--", "lightning.jpg"),
    ("Horas Festivas", 10, "festive.jpg"),
    ("Horas Domingos", 10, "sun.jpg"),
    ("Horas Nocturnas", 0, "moon.jpg"),
    ("Madrugues", 0, "sunrise.jpg"),
    ("Manutención", 0, "food.jpg"),
    ("Fraccionadas", 0, "leaf.jpg"),
]

FESTIVOS = {
    2024: {"01-01", "06-01", "29-03", "01-05", "15-08", "12-10", "01-11", "06-12", "25-12", "24-06", "11-09", "24-09"},
    2025: {"01-03","01-01", "06-01", "18-04", "01-05", "15-08", "01-11", "06-12", "25-12", "24-06", "11-09", "24-09"},
}

MESES_MAP = {
    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
}

meses_abreviados = {
    "Ene": "Enero", "Feb": "Febrero", "Mar": "Marzo", "Abr": "Abril",
    "May": "Mayo", "Jun": "Junio", "Jul": "Julio", "Ago": "Agosto",
    "Sep": "Septiembre", "Oct": "Octubre", "Nov": "Noviembre", "Dic": "Diciembre",
    "D?mbre": "Diciembre", "D7mbre": "Diciembre", "D": "Diciembre",
    "d?mbre": "Diciembre", "d7mbre": "Diciembre", "Diciembre": "Diciembre"
}

MESES_MAP_INV = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

SUNDAYS = {
    2024: {"07-01", "14-01", "21-01", "28-01", "04-02", "11-02", "18-02", "25-02",
           "03-03", "10-03", "17-03", "24-03", "31-03", "07-04", "14-04", "21-04", "28-04",
           "05-05", "12-05", "19-05", "26-05", "02-06", "09-06", "16-06", "23-06", "30-06",
           "07-07", "14-07", "21-07", "28-07", "04-08", "11-08", "18-08", "25-08", "01-09",
           "08-09", "15-09", "22-09", "29-09", "06-10", "13-10", "20-10", "27-10",
           "03-11", "10-11", "17-11", "24-11", "01-12", "08-12", "15-12", "22-12", "29-12"},
    2025: {"01-03","05-01", "12-01", "19-01", "26-01", "02-02", "09-02", "16-02", "23-02",
           "02-03", "09-03", "16-03", "23-03", "30-03", "06-04", "13-04", "20-04", "27-04",
           "04-05", "11-05", "18-05", "25-05", "01-06", "08-06", "15-06", "22-06", "29-06",
           "06-07", "13-07", "20-07", "27-07", "03-08", "10-08", "17-08", "24-08", "31-08",
           "07-09", "14-09", "21-09", "28-09", "05-10", "12-10", "19-10", "26-10",
           "02-11", "09-11", "16-11", "23-11", "30-11", "07-12", "14-12", "21-12", "28-12"}
}