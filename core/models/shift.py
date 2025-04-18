#clockpilot/core/models/shift.py
from datetime import datetime, timedelta

class Shift:
    def __init__(self, entrada, salida, tipo=None):
        self.entrada = entrada
        self.salida = salida
        self.tipo = tipo

    def duracion(self):
        try:
            fmt = "%H:%M"
            start = datetime.strptime(self.entrada, fmt)
            end = datetime.strptime(self.salida, fmt)
            if end <= start:
                end += timedelta(days=1)
            return end - start
        except Exception as e:
            print(f"Error calculando duración: {e}")
            return timedelta()
