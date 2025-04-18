# clockpilot/core/security.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from google.auth.transport import requests
from google.oauth2 import id_token
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from dotenv import load_dotenv

from database.models.user import User
from database.session import get_db
from core.config import get_settings
load_dotenv()

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
GOOGLE_CLIENT_ID = settings.google_client_id


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {str(e)}"
        )


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = verify_token(token)
    user_email = payload.get("sub")

    if not user_email:
        raise HTTPException(status_code=401, detail="Token sin 'sub' válido")

    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user


async def verify_google_token(token: str) -> dict:
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=10
        )

        if idinfo.get("iss") not in ["accounts.google.com", "https://accounts.google.com"]:
            raise ValueError("Emisor no es Google")

        return {
            "email": idinfo["email"],
            "name": idinfo.get("name", ""),
            "sub": idinfo["sub"]
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token de Google inválido: {str(e)}"
        )


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)