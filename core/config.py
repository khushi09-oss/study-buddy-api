from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gemini_api_key: str
    gemini_model: str = "gemini-1.5-flash"
    api_secret_key: str = "dev-secret-123"
    app_name: str = "Study Buddy API"

    class Config:
        env_file=".env"

settings = Settings()