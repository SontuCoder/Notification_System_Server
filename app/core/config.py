from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    APP_NAME: str
    DATABASE_URL: str
    RABBITMQ_URL: str
    JWT_SECRET_KEY: str
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_USE_TLS: str

    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str
    TWILIO_CODE: str
    AUTH_HOST: str
    class Config:
        env_file = ".env"

settings = Settings()

