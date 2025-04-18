#clockpilot/api/schemas/shift_schema.py

from pydantic import BaseModel, ConfigDict

class Shift(BaseModel):
    hora_entrada: str
    hora_salida: str
    tipo: str | None = None

    model_config = ConfigDict(from_attributes=True)