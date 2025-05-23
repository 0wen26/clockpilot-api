# clockpilot/database/base.py

from sqlalchemy.orm import as_declarative, declared_attr

@as_declarative()
class Base:
    id: int
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        """Generar automáticamente el nombre de la tabla en minúsculas"""
        return cls.__name__.lower()