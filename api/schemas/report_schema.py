# clockpilot/api/schemas/report_schema.py

from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Dict, List,Optional
from .shift_schema import Shift
from .response import ApiResponse

class DaySummary(BaseModel):
    fecha: str
    turnos: List[Shift]
    duracion_total: str
    horas_perentorias: str
    festive_hours: str
    horas_domingos: str
    horas_madrugue: str
    horas_nocturnas: str
    manutencion: int
    fraccionadas: int

    model_config = ConfigDict(from_attributes=True)

class ReportFromDB(BaseModel):
    id: int
    horas_contrato: int
    year: int
    month: int
    total_hours: Optional[str]
    total_hr_hours: Optional[str]
    complementary_hours: Optional[str]
    total_festive_hours: Optional[str]
    total_sunday_hours: Optional[str]
    total_early_days: Optional[int]
    total_night_hours: Optional[str]
    total_meal_allowance: Optional[int]
    total_split_shifts: Optional[int]
    created_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class ReportResponse(ApiResponse):
    data: ReportFromDB


class ReportListResponse(ApiResponse):
    data: List[ReportFromDB]

class ReportUpdateSchema(BaseModel):
    horas_contrato: Optional[int] = None
    year: Optional[int] = None
    total_hours: Optional[str] = None
    total_hr_hours: Optional[str] = None
    complementary_hours: Optional[str] = None
    total_festive_hours: Optional[str] = None
    total_sunday_hours: Optional[str] = None
    total_early_days: Optional[int] = None
    total_night_hours: Optional[str] = None
    total_meal_allowance: Optional[int] = None
    total_split_shifts: Optional[int] = None

    class Config:
        from_attributes = True
