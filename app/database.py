import sqlite3
from contextlib import contextmanager
from app.config import settings

@contextmanager
def get_db():
    conn = sqlite3.connect(settings.database_url)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        pass
        #conn.execute("") #make the table if it doesn't exist
                         #assume it exists for now

