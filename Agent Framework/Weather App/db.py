import sqlite3
from datetime import datetime,timezone
DB_FILE = "chat_history.db"

def init_db():
    query='''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT,
                role TEXT,
                content TEXT,
                timestamp TEXT
            )
        '''
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(query)
        conn.commit()

def save_message(conversation_id, role, content):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO messages (conversation_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
            (conversation_id, role, content,datetime.now(timezone.utc).isoformat())
        )
        conn.commit()

def load_messages(conversation_id):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY id ", (conversation_id,))
        return c.fetchall()
        
def get_all_conversation_ids():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT DISTINCT conversation_id FROM messages")
        return [row[0] for row in c.fetchall()]

def delete_conversations():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM messages")
        conn.commit()