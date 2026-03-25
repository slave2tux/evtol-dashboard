import sqlite3
import datetime

DB_PATH = "data/history.db"

def init_history_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS spec_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            range_miles INTEGER,
            payload_lbs INTEGER,
            power_type TEXT,
            market_focus TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_specs(specs: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO spec_history (company, range_miles, payload_lbs, power_type, market_focus, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        specs.get("Company"),
        specs.get("Range (Miles)"),
        specs.get("Payload (lbs)"),
        specs.get("Power Type"),
        specs.get("Market Focus"),
        datetime.datetime.utcnow().isoformat()
    ))
    conn.commit()
    conn.close()

def load_history(company: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT timestamp, range_miles, payload_lbs
        FROM spec_history
        WHERE company = ?
        ORDER BY timestamp ASC
    """, (company,))
    rows = c.fetchall()
    conn.close()
    return rows
