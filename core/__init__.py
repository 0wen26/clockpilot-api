# clockpilot/core/__init__.py

# Exportaciones principales
from .file_processing.pdf_processor import PDFProcessor as ProcesadorPDF


from .constants import (
    SUNDAYS, 
    MESES_MAP, 
    meses_abreviados, 
    FESTIVOS,
    CARD_COLORS,
    DATA
)

# Re-exportar cálculos desde su __init__
from .calculations import (
    calculate_sunday_hours,
    calculate_festive_hours,
    calculate_madrugue_hours,
    calculate_meal_allowance,
    calculate_split_shift,
    calculate_night_hours,
    calculate_complementary_hours
    
)

__all__ = [
    'ProcesadorPDF',
    'procesar_pdf_a_json',
    'SUNDAYS',
    'MESES_MAP',
    'meses_abreviados',
    'FESTIVOS',
    'CARD_COLORS',
    'DATA',
    'calculate_sunday_hours',
    'calculate_festive_hours',
    'calculate_madrugue_hours',
    'calculate_meal_allowance',
    'calculate_split_shift',
    'calculate_night_hours',
    'calculate_complementary_hours'
]

def init_core():
    """Inicializa configuraciones locales del core."""
    try:
        import locale
        locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, "Spanish_Spain.1252")
        except locale.Error:
            pass