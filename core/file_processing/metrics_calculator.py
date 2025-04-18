from datetime import timedelta
from typing import Dict
from core.calculations import (
    calculate_sunday_hours,
    calculate_festive_hours,
    calculate_madrugue_hours,
    calculate_night_hours,
    calculate_meal_allowance,
    calculate_split_shift,
    calculate_complementary_hours,
)
from core.utils import TimeConverter

class MetricsCalculator:
    def __init__(self, year: int):
        self.year = year

    def compute_all_metrics(self, contract_hours: int, data: dict) -> dict:
        return {
            "total_hours": self._sum(data, "duracion_total"),
            "total_hr_hours": self._sum(data, "horas_perentorias"),
            "complementary_hours": calculate_complementary_hours(
                contract_hours,
                self._sum(data, "duracion_total"),
                self._sum(data, "horas_perentorias")
            ),
            "total_festive_hours": calculate_festive_hours(data, str(self.year)),
            "total_sunday_hours": calculate_sunday_hours(data, str(self.year)),
            "total_early_days": calculate_madrugue_hours(data),
            "total_night_hours": calculate_night_hours(data),
            "total_meal_allowance": calculate_meal_allowance(data),
            "total_split_shifts": calculate_split_shift(data),
        }

    def _sum(self, data: dict, key: str) -> str:
        total = timedelta()
        for entry in data.values():
            value = entry.get(key, timedelta())
            if isinstance(value, str):
                value = TimeConverter.hh_mm_to_timedelta(value)
            total += value
        return TimeConverter.timedelta_to_hh_mm(total)