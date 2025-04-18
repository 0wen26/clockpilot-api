# clockpilot/database/crud/user_crud.py

from sqlalchemy.orm import Session
from database.models.user import User
from database.schemas.user_schema import UserCreate
from core.security import get_password_hash, verify_password

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_data: UserCreate):
    db_user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        is_active=True,
        provider="email",
        role=user_data.role or "user",
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_google_user(db: Session, google_data: dict):
    user = get_user_by_email(db, google_data["email"])
    if not user:
        user = User(
            email=google_data["email"],
            full_name=google_data.get("name", ""),
            provider="google",
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
