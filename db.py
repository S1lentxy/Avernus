import sqlite3
from pathlib import Path

DB_PATH = Path("avernus.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    
    # Todas tus tablas aquí (las que ya tenías)
    c.execute('''CREATE TABLE IF NOT EXISTS guild_config (
        guild_id TEXT PRIMARY KEY,
        prefix TEXT DEFAULT "!",
        log_channel_id TEXT
    )''')
    
    # ... (pega el resto de tus CREATE TABLE que tenías)
    
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada")

if __name__ == "__main__":
    init_db()
