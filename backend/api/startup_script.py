# backend/api/startup_script.py
import os
from pathlib import Path

def create_storage_dirs():
    storage_root = Path(__file__).resolve().parent / "storage"
    episodes_dir = storage_root / "episodes"
    voices_dir = storage_root / "voices"

    for d in [storage_root, episodes_dir, voices_dir]:
        d.mkdir(parents=True, exist_ok=True)

    print(f"[startup] Storage directories created at {storage_root}")

def create_database():
    import sqlite3
    db_path = Path(__file__).resolve().parent / "globalpodcaster.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS episodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        podcast_id INTEGER,
        title TEXT,
        transcript TEXT,
        translation TEXT,
        audio_url TEXT
    )
    """)
    conn.commit()
    conn.close()
    print(f"[startup] Database initialized at {db_path}")

if __name__ == "__main__":
    create_storage_dirs()
    create_database()
