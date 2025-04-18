from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    provider = Column(String, default="email")
    role = Column(String, default="user")

    reports = relationship("Report", back_populates="user", cascade="all, delete-orphan")

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    horas_contrato = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)

    total_hours = Column(String, nullable=False)
    total_hr_hours = Column(String, nullable=False)
    complementary_hours = Column(String, nullable=False)
    total_festive_hours = Column(String, nullable=False)
    total_sunday_hours = Column(String, nullable=False)
    total_early_days = Column(Integer, nullable=False)
    total_night_hours = Column(String, nullable=False)
    total_meal_allowance = Column(Integer, nullable=False)
    total_split_shifts = Column(Integer, nullable=False)

    user = relationship("User", back_populates="reports")
    day_summaries = relationship("DaySummary", back_populates="report", cascade="all, delete-orphan", overlaps="days")


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

    report = relationship("Report", back_populates="day_summaries")
    shifts = relationship("Shift", back_populates="day", cascade="all, delete-orphan")

class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("day_summaries.id"), nullable=False)
    hora_entrada = Column(String, nullable=False)
    hora_salida = Column(String, nullable=False)
    tipo = Column(String, nullable=True)

    day = relationship("DaySummary", back_populates="shifts")
    