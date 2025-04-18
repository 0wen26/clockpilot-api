# clockpilot/core/utils.py
from datetime import timedelta, datetime, date
import re
from typing import List, Dict, Optional
import locale
from core.constants import meses_abreviados, MESES_MAP


class TimeConverter:
    """Clase para conversiones de tiempo"""

    @staticmethod
    def minutes_to_hh_mm(minutes: int) -> str:
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"

    @staticmethod
    def hh_mm_to_minutes(hhmm: str) -> int:
        try:
            hours, minutes = map(int, hhmm.split(":"))
            return hours * 60 + minutes
        except:
            return 0

    @staticmethod
    def hh_mm_to_timedelta(time_str: str) -> timedelta:
        """Convierte HH:MM a timedelta"""
        if not isinstance(time_str, str):
            return timedelta()
        try:
            hours, minutes = map(int, time_str.split(':'))
            return timedelta(hours=hours, minutes=minutes)
        except (ValueError, AttributeError):
            return timedelta()

    @staticmethod
    def timedelta_to_hh_mm(td: timedelta) -> str:
        """Convierte timedelta a formato HH:MM"""
        total_seconds = td.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return f"{hours:02d}:{minutes:02d}"

    @staticmethod
    def calculate_shift_duration(start: str, end: str) -> timedelta:
        """Calcula duración entre dos horas, considerando si cruza medianoche"""
        try:
            h_start, m_start = map(int, start.split(':'))
            h_end, m_end = map(int, end.split(':'))

            start_min = h_start * 60 + m_start
            end_min = h_end * 60 + m_end
            if end_min < start_min:
                end_min += 24 * 60

            return timedelta(minutes=end_min - start_min)
        except ValueError:
            return timedelta()

    @staticmethod
    def calculate_hr_hours(shifts: List[Dict]) -> timedelta:
        """Calcula horas HR"""
        total = timedelta()
        for shift in shifts:
            if shift.get("tipo") == "HR":
                try:
                    start = datetime.strptime(shift["hora_entrada"], "%H:%M")
                    end = datetime.strptime(shift["hora_salida"], "%H:%M")
                    if end < start:
                        end += timedelta(days=1)
                    total += end - start
                except ValueError:
                    continue
        return total


class DateProcessor:
    """Clase para procesamiento de fechas"""

    @staticmethod
    def parse_date(date_str: str, year: int = None) -> Optional[date]:
        """Parsea fechas en varios formatos"""
        try:
            clean_date = date_str.replace("Dom ", "").replace("dom ", "").strip()
            if re.match(r'^\d{2}-\d{2}$', clean_date):  # Formato DD-MM
                day, month = clean_date.split('-')
            else:
                day, month_name = clean_date.split('-')
                month_name = month_name.lower().capitalize()
                month_normalized = meses_abreviados.get(month_name[:3], month_name)
                month = MESES_MAP.get(month_normalized.lower())
                if not month:
                    return None

            day = f"{int(day):02d}"
            month = f"{int(month):02d}" if month.isdigit() else month
            year = year or datetime.now().year

            return datetime.strptime(f"{day}-{month}-{year}", "%d-%m-%Y").date()
        except Exception:
            return None

    @staticmethod
    def setup_locale():
        """Configura locale para manejo de fechas en español"""
        for loc in ["es_ES.UTF-8", "Spanish_Spain.1252"]:
            try:
                locale.setlocale(locale.LC_TIME, loc)
                break
            except locale.Error:
                continue
