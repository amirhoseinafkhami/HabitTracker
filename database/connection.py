import sqlite3

from contextlib import contextmanager

from config.settings import settings

@contextmanager
def get_connection():

    conn = sqlite3.connect(settings.DATABASE_PATH)

    # return rows as dictionary like objects
    conn.row_factory = sqlite3.Row

    # enable foreign key constraints
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()