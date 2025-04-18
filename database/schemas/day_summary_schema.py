# clockpilot/database/schemas/day_summary_schema.py

from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import datetime
from .shift_schema import Shift

class DaySummaryBase(BaseModel):
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    total_duration: str = Field(..., pattern=r"^\d{1,3}:\d{2}$")
    overtime_hours: str = Field("00:00", pattern=r"^\d{1,3}:\d{2}$")
    festive_hours: str = Field("00:00", pattern=r"^\d{1,3}:\d{2}$")
    sunday_hours: str = Field("00:00", pattern=r"^\d{1,3}:\d{2}$")
    early_hours: str = Field("00:00", pattern=r"^\d{1,3}:\d{2}$")
    night_hours: str = Field("00:00", pattern=r"^\d{1,3}:\d{2}$")
    meal_allowance: int = Field(0, ge=0)
    split_shifts: int = Field(0, ge=0)

    model_config = ConfigDict(from_attributes=True)

class DaySummaryCreate(DaySummaryBase):
    report_id: int

class DaySummaryUpdate(BaseModel):
    total_duration: Optional[str] = Field(None, pattern=r"^\d{1,3}:\d{2}$")
    overtime_hours: Optional[str] = Field(None, pattern=r"^\d{1,3}:\d{2}$")
    festive_hours: Optional[str] = Field(None, pattern=r"^\d{1,3}:\d{2}$")
    sunday_hours: Optional[str] = Field(None, pattern=r"^\d{1,3}:\d{2}$")
    early_hours: Optional[str] = Field(None, pattern=r"^\d{1,3}:\d{2}$")
    night_hours: Optional[str] = Field(None, pattern=r"^\d{1,3}:\d{2}$")
    meal_allowance: Optional[int] = Field(None, ge=0)
    split_shifts: Optional[int] = Field(None, ge=0)

class DaySummary(DaySummaryBase):
    id: int
    report_id: int
    created_at: datetime = Field(default_factory=datetime.now)
    shifts: List[Shift] = Field(default_factory=list)
