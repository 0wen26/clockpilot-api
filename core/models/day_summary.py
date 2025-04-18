#clockpilot/core/models/day_summary.py
from datetime import timedelta
from core.utils import timedelta_to_hh_mm

class DaySummary:
    def __init__(self, fecha, turnos, duracion_total="00:00", horas_perentorias="00:00", 
                 festive_hours="00:00", horas_domingos="00:00", horas_madrugue=0,
                 horas_nocturnas="00:00", manutencion=0, fraccionadas=0):
        self.fecha = fecha
        self.turnos = turnos
        self.duracion_total = duracion_total
        self.horas_perentorias = horas_perentorias
        self.festive_hours = festive_hours
        self.horas_domingos = horas_domingos
        self.horas_madrugue = horas_madrugue
        self.horas_nocturnas = horas_nocturnas
        self.manutencion = manutencion
        self.fraccionadas = fraccionadas

    def calculate_totals(self, year):
        """Calcula todos los totales para este día"""
        print(f"🧮 Calculando totales para {self.fecha} con {len(self.turnos)} turnos")
        from core.calculations import (
            early_shifts,
            night_hours,
            meal_allowance,
            split_shifts,
            festive_hours,
            sunday_hours
        )
        
        # Convertir turnos a formato esperado por los cálculos
        turnos_data = {self.fecha: {"turnos": [
            {
                "hora_entrada": getattr(t, "entrada", ""),
                "hora_salida": getattr(t, "salida", ""),
                "tipo": getattr(t, "tipo", "Normal")
            } for t in self.turnos
        ]}}

        
        # Calcular duración total
        total = timedelta()
        for turno in self.turnos:
            total += turno.duracion()
        self.duracion_total = timedelta_to_hh_mm(total)
        
        # Calcular otros valores
        self.horas_madrugue = early_shifts.calculate_madrugue_hours(turnos_data)
        self.horas_nocturnas = night_hours.calculate_night_hours(turnos_data)
        self.manutencion = meal_allowance.calculate_meal_allowance(turnos_data)
        self.fraccionadas = split_shifts.calculate_split_shift(turnos_data)
        self.festive_hours = festive_hours.calculate_festive_hours(turnos_data, year)
        self.horas_domingos = sunday_hours.calculate_sunday_hours(turnos_data, year)
        
        return self