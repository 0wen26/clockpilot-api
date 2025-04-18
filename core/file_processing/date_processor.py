# clockpilot/core/file_processing/date_processor.py
from datetime import datetime, date
import re
import locale
from typing import Optional

from ..constants import meses_abreviados, MESES_MAP

class DateProcessor:
    @staticmethod
    def setup_locale():
        """Configura locale para manejo de fechas en español"""
        for loc in ["es_ES.UTF-8", "Spanish_Spain.1252"]:
            try:
                locale.setlocale(locale.LC_TIME, loc)
                break
            except locale.Error:
                continue

    @staticmethod
    def parse_date(date_str: str, year: int = None) -> Optional[date]:
        """Parsea fechas en varios formatos a objeto date"""
        try:
            # Limpiar texto
            clean_date = date_str.replace("Dom ", "").replace("dom ", "").strip()
            
            # Manejar diferentes formatos
            if re.match(r'^\d{2}-\d{2}$', clean_date):  # Formato DD-MM
                day, month = clean_date.split('-')
            else:  # Formato texto
                day, month_name = clean_date.split('-')
                month_name = month_name.lower().capitalize()
                month_normalized = meses_abreviados.get(month_name[:3], month_name)
                month = MESES_MAP.get(month_normalized.lower())
                if not month:
                    return None
            
            # Construir fecha
            day = f"{int(day):02d}"
            month = f"{int(month):02d}" if month.isdigit() else month
            year = year or datetime.now().year
            
            return datetime.strptime(f"{day}-{month}-{year}", "%d-%m-%Y").date()
        except Exception:
            return None