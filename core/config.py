from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    anthropic_api_key: str
    api_secret_key: str = "dev-secret-123"
    app_name: str = "Study Buddy API"

    class Config:
        env_file=".env"

settings = Settings()