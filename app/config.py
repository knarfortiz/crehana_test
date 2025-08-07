from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "ToDo API"
    db_url: str = f"sqlite:///{BASE_DIR / 'todo.db'}"
    debug_db: bool = True

    smtp_host: str = "localhost"
    smtp_port: int = 1025
    from_email: str = "no-reply@miapp.local"

    secret_key: str = "supersecreto"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
