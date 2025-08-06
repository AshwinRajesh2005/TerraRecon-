import sqlite3
from config import DATABASE_PATH

def setup_database():
    """Creates the database table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registered_personnel (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                face_encoding BLOB NOT NULL UNIQUE,
                image_filename TEXT
            )
        """)
        conn.commit()
        print(f"Database {DATABASE_PATH} checked/created")
    except sqlite3.Error as e:
        print(f"Database setup error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    setup_database()