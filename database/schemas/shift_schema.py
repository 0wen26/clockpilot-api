# clockpilot/database/schemas/shift_schema.py

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class ShiftBase(BaseModel):
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    start_time: str = Field(..., pattern=r"^\d{2}:\d{2}$")
    end_time: str = Field(..., pattern=r"^\d{2}:\d{2}$")
    shift_type: Optional[str] = None
    total_duration: str = Field(..., pattern=r"^\d{1,3}:\d{2}$")
    overtime_hours: str = Field("00:00", pattern=r"^\d{1,3}:\d{2}$")
    festive_hours: str = Field("00:00", pattern=r"^\d{1,3}:\d{2}$")
    sunday_hours: str = Field("00:00", pattern=r"^\d{1,3}:\d{2}$")
    early_hours: str = Field("00:00", pattern=r"^\d{1,3}:\d{2}$")
    night_hours: str = Field("00:00", pattern=r"^\d{1,3}:\d{2}$")
    meal_allowance: int = Field(0, ge=0)
    split_shifts: int = Field(0, ge=0)

    model_config = ConfigDict(from_attributes=True)

class ShiftCreate(ShiftBase):
    report_id: int

class Shift(ShiftBase):
    id: int
    report_id: int
    created_at: datetime = Field(default_factory=datetime.now)