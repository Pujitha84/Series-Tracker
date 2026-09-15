import sqlite3

DATABASE = "series.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS series (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT,
            status TEXT NOT NULL,
            rating REAL DEFAULT 0,
            episodes INTEGER DEFAULT 0,
            total_episodes INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()