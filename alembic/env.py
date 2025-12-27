from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from gestao_atletas_api.configs.settings import settings
from gestao_atletas_api.contrib.models import BaseModel


# Configuração base do Alembic
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata usada pelo autogenerate
target_metadata = BaseModel.metadata


# Força Alembic a usar DATABASE_URL_SYNC (psycopg)
if not settings.DATABASE_URL_SYNC:
    raise RuntimeError("DATABASE_URL_SYNC nçao foi definida")

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL_SYNC)


# Migrations OFFLINE
def run_migrations_offline():
    """
    Executa migrations no modo offline.
    Não cria conexão com o banco.
    """
    context.configure(
        url=settings.DATABASE_URL_SYNC,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

# Migrations ONLINE
def run_migrations_online():
    """
    Executa migrations no modo online.
    Usa engine SINCRONO (psycopg2).
    """

    connectable = engine_from_config(
        {"sqlalchemy.url": settings.DATABASE_URL_SYNC},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

# Dispatcher
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()