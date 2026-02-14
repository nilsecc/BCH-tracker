import sqlite3
from src.database.database import DB_NAME

def insert_transaction(txid, address, amount, tx_type, block_height):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO transactions (txid, address, amount, type, block_height)
        VALUES (?, ?, ?, ?, ?)
    ''', (txid, address, amount, type, block_height))
    conn.commit()
    conn.close()

def insert_address(address, total_received=0, total_sent=0, tx_count=0):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO addresses (address, total_received, total_sent, tx_count)
        VALUES (?, ?, ?, ?)
    ''', (address, total_received, total_sent, tx_count))
    conn.commit()
    conn.close()

def get_transactions(address):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions WHERE address=?', (address,))
    result = cursor.fetchall()
    conn.close()
    return result

def get_address_info(address):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM addresses WHERE address=?', (address,))
    result = cursor.fetchone()
    conn.close()
    return result
