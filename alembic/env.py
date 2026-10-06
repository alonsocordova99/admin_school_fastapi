from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from admin_school_fastapi.app.db.base import Base  # Base declarativa
from admin_school_fastapi.app.core.utils.config import settings  # Configuración

# Importar todos los modelos para que Alembic los detecte
from admin_school_fastapi.app.db.models import *

# Configuración de logging
config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    url = settings.DATABASE_URL
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        {"sqlalchemy.url": settings.DATABASE_URL},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    print("1")
    run_migrations_offline()
else:
    print("2")
    run_migrations_online()
