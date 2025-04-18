# reset_db.py

from database.session import SessionLocal
from database.models import Report, DaySummary, Shift, User  # importa todos tus modelos

db = SessionLocal()

# Elimina en orden correcto (dependencias)
db.query(Shift).delete()
db.query(DaySummary).delete()
db.query(Report).delete()
# Cuidado con esto si no quieres borrar usuarios:
# db.query(User).delete()

db.commit()
db.close()

print("🧹 Base de datos reiniciada (sin borrar usuarios)")
