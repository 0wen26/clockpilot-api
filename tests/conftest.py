import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.base import Base
from database.models import User
from core.security import get_password_hash
import sys
from pathlib import Path

# Configuración de paths
sys.path.append(str(Path(__file__).parent.parent))
from app.main import app

# Configuración de la base de datos de prueba
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def engine():
    return create_engine(TEST_DATABASE_URL)

@pytest.fixture(scope="function")
def db(engine):
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_user(db):
    # Eliminar usuario existente si existe
    db.query(User).filter(User.email == "test@example.com").delete()
    db.commit()
    
    # Crear nuevo usuario de prueba
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("123"),
        full_name="Test User",
        is_active=True,
        provider="email"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def auth_token(test_user):
    from core.security import create_access_token
    return create_access_token(data={"sub": test_user.email})