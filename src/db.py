import sqlite3
from config import BASE_PATH

DB_PATH = BASE_PATH / "notified_topics.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notified (
            topic_id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def is_notified(topic_id: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM notified WHERE topic_id = ?", (topic_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def mark_as_notified(topic_id: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO notified (topic_id) VALUES (?)", (topic_id,))
    conn.commit()
    conn.close()