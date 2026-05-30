from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "GitHub Repository Analyzer"
    GITHUB_TOKEN: Optional[str] = None
    DATABASE_URL: str = "sqlite:///./github_analyzer.db"

    class Config:
        env_file = ".env"

settings = Settings()
