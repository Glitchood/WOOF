from pathlib import Path
from sqlmodel import Session, SQLModel, create_engine

from .config import settings

# Ensure the data directory exists
data_dir = Path(settings.DATABASE_URL.replace("sqlite:///", "")).parent
data_dir.mkdir(parents=True, exist_ok=True)

engine = create_engine(settings.DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
