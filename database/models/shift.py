# clockpilot/database/models/shift.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("day_summaries.id"), nullable=False)
    hora_entrada = Column(String, nullable=False)
    hora_salida = Column(String, nullable=False)
    tipo = Column(String, nullable=True)

    # Relaciones
    day = relationship("DaySummary", back_populates="shifts")
