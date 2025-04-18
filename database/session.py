# clockpilot/database/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./instance/clockpilot.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Generador de sesiones para dependencias de FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
