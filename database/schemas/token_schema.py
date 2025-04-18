# clockpilot/database/schemas/token_schema.py

from pydantic import BaseModel, ConfigDict, Field

class Token(BaseModel):
    """Token de autenticación JWT"""
    access_token: str = Field(..., description="Token de acceso")
    token_type: str = Field(default="bearer", description="Tipo de token")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOi...",
                "token_type": "bearer"
            }
        }
    )