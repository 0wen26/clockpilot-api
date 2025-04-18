# clockpilot/database/schemas/report_schema.py
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Dict, Optional
from datetime import datetime
from .shift_schema import Shift

class ReportBase(BaseModel):
    """Modelo base para reportes"""
    total_hours: str = Field(..., pattern=r"^\d{1,3}:\d{2}$", description="Total hours (HH:MM)")
    total_hr_hours: str = Field("00:00", pattern=r"^\d{1,3}:\d{2}$", description="Overtime hours (HH:MM)")
    complementary_hours: str = Field("00:00", pattern=r"^\d{1,3}:\d{2}$", description="Complementary hours (HH:MM)")
    total_festive_hours: str = Field("00:00", pattern=r"^\d{1,3}:\d{2}$", description="Holiday hours (HH:MM)")
    total_sunday_hours: str = Field("00:00", pattern=r"^\d{1,3}:\d{2}$", description="Sunday hours (HH:MM)")
    total_early_days: int = Field(0, ge=0, description="Early morning shifts count")
    total_night_hours: str = Field("00:00", pattern=r"^\d{1,3}:\d{2}$", description="Night hours (HH:MM)")
    total_meal_allowance: int = Field(0, ge=0, description="Total meal allowances")
    total_split_shifts: int = Field(0, ge=0, description="Total split shifts")
    contract_hours: int = Field(..., alias="horas_contrato", description="Monthly contract hours")
    year: int = Field(..., ge=2000, le=datetime.now().year, description="Report year")
    user_id: int = Field(..., description="User ID")
    month: int = Field(..., ge=1, le=12, description="Mes del reporte")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "total_hours": "160:45",
                "total_hr_hours": "12:30",
                "complementary_hours": "05:15",
                "total_festive_hours": "08:00",
                "total_sunday_hours": "24:00",
                "total_early_days": 4,
                "total_night_hours": "32:45",
                "total_meal_allowance": 8,
                "total_split_shifts": 2,
                "horas_contrato": 160,
                "year": 2023,
                "user_id": 1,
                "month": 1,
            }
        }
    )

class ReportCreate(ReportBase):
    details: Dict[str, Dict] = Field(
        default_factory=dict,
        alias="detalles",
        description="Daily details (YYYY-MM-DD: {data})"
    )

class Report(ReportBase):
    id: int = Field(..., description="Report ID")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation date")
    updated_at: Optional[datetime] = Field(None, description="Last update")
    shifts: List[Shift] = Field(default_factory=list, description="Associated shifts")

class ReportUpdateSchema(BaseModel):
    """Schema para actualizar reportes parcialmente"""
    total_hours: Optional[str] = Field(None, pattern=r"^\d{1,3}:\d{2}$")
    total_hr_hours: Optional[str] = Field(None, pattern=r"^\d{1,3}:\d{2}$")
    complementary_hours: Optional[str] = Field(None, pattern=r"^\d{1,3}:\d{2}$")
    total_festive_hours: Optional[str] = Field(None, pattern=r"^\d{1,3}:\d{2}$")
    total_sunday_hours: Optional[str] = Field(None, pattern=r"^\d{1,3}:\d{2}$")
    total_early_days: Optional[int] = Field(None, ge=0)
    total_night_hours: Optional[str] = Field(None, pattern=r"^\d{1,3}:\d{2}$")
    total_meal_allowance: Optional[int] = Field(None, ge=0)
    total_split_shifts: Optional[int] = Field(None, ge=0)
    contract_hours: Optional[int] = Field(None, alias="horas_contrato")
    year: Optional[int] = Field(None, ge=2000, le=datetime.now().year)
    month: Optional[int] = Field(None, ge=1, le=12)

    model_config = ConfigDict(from_attributes=True)
