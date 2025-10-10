from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI SQLite App"
    database_url: str = "data/sample.db"
    debug: bool = True
    log_request_body: bool = True
    log_response_body: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
