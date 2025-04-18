# clockpilot/database/models/user.py

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    provider = Column(String, default="email")
    role = Column(String, default="user") 
    
    # Relaciones
    reports = relationship("Report", back_populates="user")