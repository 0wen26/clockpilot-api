# clockpilot/api/schemas/response.py

from pydantic import BaseModel, ConfigDict, Field
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class ApiResponse(BaseModel):
    success: bool = Field(default=True, description="Indica si la operación fue exitosa")
    message: str = Field(default="Operación exitosa", description="Mensaje descriptivo")
    data: Optional[T] = Field(default=None, description="Datos de respuesta")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Datos obtenidos correctamente",
                "data": {"id": 1, "name": "Ejemplo"}
            }
        }
    )

class ErrorResponse(ApiResponse):
    success: bool = Field(default=False)
    error_code: str = Field(..., description="Código único de error")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": False,
                "message": "Error de autenticación",
                "error_code": "AUTH_001",
                "data": None
            }
        }
    )