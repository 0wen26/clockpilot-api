from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from sqlalchemy import text
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS shifts, day_summaries, reports, users CASCADE;"))
    print("¡Tablas eliminadas!")
