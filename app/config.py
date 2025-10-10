from pydantic_settings import BaseSettings

from pathlib import Path

# Get the absolute path to the app directory
BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    app_name: str = "WOOF API"
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/data/sample.db"
    SECRET_KEY: str = "your-secret-key-keep-it-secret"  # Change this in production!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    debug: bool = True
    log_request_body: bool = True
    log_response_body: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
