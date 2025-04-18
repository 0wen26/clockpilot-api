# clockpilot/database/schemas/user_schema.py
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    """Roles de usuario disponibles"""
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

class UserBase(BaseModel):
    """Esquema base para usuarios con campos esenciales"""
    email: EmailStr = Field(..., description="Email válido del usuario", max_length=255)
    full_name: Optional[str] = Field(None, description="Nombre completo del usuario", max_length=100)
    phone: Optional[str] = Field(
        None,
        description="Teléfono con código de país (+1234567890)",
        pattern=r"^\+\d{1,3}\d{9,15}$"
    )

    model_config = ConfigDict(use_enum_values=True)

class UserCreate(UserBase):
    """Esquema para creación de usuarios con validación de contraseña"""
    password: str = Field(
        ...,
        min_length=8,
        description="Contraseña segura (mínimo 8 caracteres, 1 mayúscula y 1 número)"
    )
    role: Optional[UserRole] = UserRole.USER

    @field_validator('password')
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if not any(c.isupper() for c in v):
            raise ValueError("Debe contener al menos una mayúscula")
        if not any(c.isdigit() for c in v):
            raise ValueError("Debe contener al menos un número")
        return v

class UserOut(UserBase):
    """Esquema para respuesta de usuarios (sin datos sensibles)"""
    id: int = Field(..., description="ID único del usuario")
    is_active: bool = Field(True, description="Indica si el usuario está activo")
    role: UserRole = Field(UserRole.USER, description="Rol del usuario")
    created_at: datetime = Field(default_factory=datetime.now, description="Fecha de creación")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "email": "usuario@ejemplo.com",
                "full_name": "Juan Pérez",
                "is_active": True,
                "role": "user",
                "created_at": "2023-01-01T00:00:00"
            }
        }
    )

# Esquemas para funcionalidades específicas (se pueden añadir según necesidad)
class UserLogin(BaseModel):
    """Esquema para autenticación de usuarios"""
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., description="Contraseña")

class UserPasswordResetRequest(BaseModel):
    """Esquema para solicitud de reseteo de contraseña"""
    email: EmailStr = Field(..., description="Email registrado")

class UserPasswordResetConfirm(BaseModel):
    """Esquema para confirmación de reseteo de contraseña"""
    token: str = Field(..., description="Token de verificación")
    new_password: str = Field(..., description="Nueva contraseña segura")

    @field_validator('new_password')
    def validate_password(cls, v: str) -> str:
        return UserCreate.validate_password(v)