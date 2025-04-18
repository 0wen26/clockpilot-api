# clockpilot/database/models/report.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base
from datetime import datetime

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    horas_contrato = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)

    # Totals
    total_hours = Column(String, nullable=False)
    total_hr_hours = Column(String, nullable=False)
    complementary_hours = Column(String, nullable=False)
    total_festive_hours = Column(String, nullable=False)
    total_sunday_hours = Column(String, nullable=False)
    total_early_days = Column(Integer, nullable=False)  # Cambiado de String a Integer
    total_night_hours = Column(String, nullable=False)
    total_meal_allowance = Column(Integer, nullable=False)
    total_split_shifts = Column(Integer, nullable=False)

    # Relationships
    user = relationship("User", back_populates="reports")
    days = relationship("DaySummary", back_populates="report", cascade="all, delete-orphan")
    day_summaries = relationship("DaySummary", back_populates="report", cascade="all, delete-orphan")