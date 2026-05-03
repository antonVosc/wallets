from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = (
        "postgresql+asyncpg://wallet:wallet@db:5432/wallet_db"
    )
    DATABASE_URL_SYNC: str = (
        "postgresql://wallet:wallet@db:5432/wallet_db"
    )

    class Config:
        env_file = ".env"


settings = Settings()
