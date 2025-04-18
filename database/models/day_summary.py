# clockpilot/database/models/day_summary.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class DaySummary(Base):
    __tablename__ = "day_summaries"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)
    fecha = Column(String, nullable=False)

    duracion_total = Column(String, nullable=False)
    horas_perentorias = Column(String, nullable=False)
    festive_hours = Column(String, nullable=False)
    horas_domingos = Column(String, nullable=False)
    horas_madrugue = Column(String, nullable=False)
    horas_nocturnas = Column(String, nullable=False)
    manutencion = Column(Integer, nullable=False)
    fraccionadas = Column(Integer, nullable=False)

    # Relaciones
    report = relationship("Report", back_populates="days")
    shifts = relationship("Shift", back_populates="day", cascade="all, delete-orphan")
    report = relationship("Report", back_populates="day_summaries")