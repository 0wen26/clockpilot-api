# clockpilot/database/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy.engine.url import make_url

from dotenv import load_dotenv
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

url = make_url(SQLALCHEMY_DATABASE_URL)
connect_args = {"check_same_thread": False} if url.get_backend_name() == "sqlite" else {}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Generador de sesiones para dependencias de FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
