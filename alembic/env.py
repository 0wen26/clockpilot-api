import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
import sys
import os
from app.models import Base 
# Carga las variables de entorno
load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Esta es la configuración de Alembic
config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))  # ✅ inyecta la URL

# Configuración de logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Importa tu metadata desde modelos
#from database import Base  # Asegúrate que esto esté correcto según tu estructura

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
