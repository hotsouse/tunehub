from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:de28alwth@localhost:5432/myproject "
    SECRET_KEY: str = "supersecretdevkey"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24*7
    FIRST_SUPERUSER_EMAIL: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "adminpass"

    class Config:
        env_file = ".env"

settings = Settings()
