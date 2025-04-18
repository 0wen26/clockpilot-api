# clockpilot/api/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
import logging
from datetime import timedelta

from core.security import (
    create_access_token,
    verify_google_token
)
from database.session import get_db
from database.crud.user_crud import (
    authenticate_user,
    authenticate_google_user,
    get_user_by_email,
    create_user
)
from database.schemas.user_schema import UserCreate, UserOut
from database.schemas.token_schema import Token
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
logger = logging.getLogger(__name__)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            logger.warning(f"Login fallido para: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos"
            )

        logger.info(f"Login exitoso: {user.email}")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(
            data={
                "sub": user.email,
                "user_id": user.id,
                "role": user.role
            },
            expires_delta=access_token_expires
        )

        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        logger.error(f"Error en login: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.post("/login/google", response_model=Token)
async def login_google(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        data = await request.json()
        google_token = data.get("token")

        if not google_token:
            raise HTTPException(status_code=400, detail="Token de Google requerido")

        google_data = await verify_google_token(google_token)
        user = authenticate_google_user(db, google_data)

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(
            data={
                "sub": user.email,
                "user_id": user.id,
                "role": user.role 
            },
            expires_delta=access_token_expires
        )

        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        logger.error(f"Error en login con Google: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Error al autenticar con Google"
        )


@router.post("/register", response_model=UserOut)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    try:
        new_user = create_user(db, user_data)
        return new_user
    except Exception as e:
        logger.error(f"Error al registrar usuario: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno al registrar usuario")
