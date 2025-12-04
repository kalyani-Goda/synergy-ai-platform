import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Synergy AI Platform"
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///synergy_ai.db")
    APP_ENV: str = os.getenv("APP_ENV", "development")

settings = Settings()