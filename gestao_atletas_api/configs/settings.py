from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    ENV: str = "local"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432

    DATABASE_URL: str
    DATABASE_URL_SYNC: str

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_async_db_url(cls, v: str) -> str:
        if not v.startswith("postgresql+asyncpg://"):
            raise ValueError(
                "DATABASE_URL deve usar asyncpg "
                "(postgresql+asyncpg://)"
            )
        return v
    
    @field_validator("DATABASE_URL_SYNC")
    @classmethod
    def validate_sync_db_url(cls, v: str) -> str:
        if not v.startswith(("postgresql+psycopg2://", "postgresql+psycopg://")):
            raise ValueError(
                "DATABASE_URL_SYNC deve usar psycopg2 ou psycopg "
            )
        return v
    

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="forbid",
    )

settings = Settings()