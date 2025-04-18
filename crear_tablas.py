from database.session import engine, Base
from database.models import report, shift  # Asegura que los modelos se importen

Base.metadata.create_all(bind=engine)
print("¡Tablas creadas en clockpilot.db!")
