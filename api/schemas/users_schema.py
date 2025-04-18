# clockpilot/api/schemas/users_schema.py

from pydantic import BaseModel, EmailStr, field_validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return v

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None
    is_active: bool
    provider: str

    class Config:
        from_attributes = True
