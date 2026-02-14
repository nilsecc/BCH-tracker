import sqlite3

DB_NAME = 'BCH-tracker.db'
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS addresses (
            id INTEGER PRIMARY KEY,
            address TEXT UNIQUE,
            total_received REAL DEFAULT 0,
            total_sent REAL DEFAULT 0,
            tx_count INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            txid TEXT UNIQUE,
            address TEXT,
            amount REAL,
            type TEXT, -- 'sent' o 'received'
            block_height INTEGER
        )
    ''')

    conn.commit()
    conn.close()
