from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI SQLite App"
    database_url: str = "data/app.db"
    debug: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
