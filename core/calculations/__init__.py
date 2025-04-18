# Exportamos TODAS las clases/funciones necesarias
from .sunday_hours import calculate_sunday_hours
from .festive_hours import calculate_festive_hours
from .early_shifts import  calculate_madrugue_hours
from .meal_allowance import calculate_meal_allowance
from .split_shifts import  calculate_split_shift
from .night_hours import calculate_night_hours
from .complementary_hours import calculate_complementary_hours


# Lista explícita de lo que se exporta con 'from calculations import *'
__all__ = [
    'calculate_complementary_hours',
    'calculate_festive_hours',
    'calculate_meal_allowance',
    'calculate_madrugue_hours',
    'calculate_night_hours',
    'calculate_split_shift',
    'calculate_sunday_hours',
]