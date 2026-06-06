from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    APP_NAME: str
    DATABASE_URL: str
    RABBITMQ_URL: str
    JWT_SECRET_KEY: str
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    class Config:
        env_file = ".env"

settings = Settings()

