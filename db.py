import sqlite3
import os
from datetime import datetime

DB_FILE = "jobs.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            command TEXT,
            state TEXT,
            attempts INTEGER,
            max_retries INTEGER,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS dlq (
            id TEXT PRIMARY KEY,
            command TEXT,
            last_state TEXT,
            attempts INTEGER,
            max_retries INTEGER,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def execute(query, params=(), fetch=False):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(query, params)
    if fetch:
        result = c.fetchall()
    else:
        result = None
    conn.commit()
    conn.close()
    return result
