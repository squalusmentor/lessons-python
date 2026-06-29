from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration settings"""
    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "test_task_db"
    SEED_DB: bool = False

    # JWT
    JWT_SECRET: str = "your_jwt_secret_key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_TTL_MINUTES: int = 15
    REFRESH_TOKEN_TTL_DAYS: int = 7

    # App
    APP_PORT: int = 8000
    APP_HOST: str = "127.0.0.1"

    @property
    def databese_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
