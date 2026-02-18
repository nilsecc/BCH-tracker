import sqlite3
from src.database.database import DB_NAME

def upsert_address(address, total_received=0, total_sent=0, tx_count=0):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO addresses (address, total_received, total_sent, tx_count)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(address) DO UPDATE SET
            total_received = excluded.total_received,
            total_sent     = excluded.total_sent,
            tx_count       = excluded.tx_count
    ''', (address, total_received, total_sent, tx_count))
    conn.commit()
    conn.close()

def insert_transaction(txid, address, amount, tx_type, block_height):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO transactions (txid, address, amount, type, block_height)
        VALUES (?, ?, ?, ?, ?)
    ''', (txid, address, amount, tx_type, block_height))
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

def insert_activity(activity, address_to_check, blocks_to_check):
    if not activity:
        print("No activity found in the checked blocks.")
    else:
        total_received = sum(e['amount'] for e in activity if e['type'] == 'received')
        total_sent     = sum(e['amount'] for e in activity if e['type'] == 'sent')
        tx_count       = len(activity)

        upsert_address(
            address=address_to_check,
            total_received=total_received,
            total_sent=total_sent,
            tx_count=tx_count,
        )

        for entry in activity:
            insert_transaction(
                txid=entry['txid'],
                address=entry['address'],
                amount=entry['amount'],
                tx_type=entry['type'],
                block_height=entry['block_height'],
            )
            print(
                f"Block {entry['block_height']} | "
                f"{entry['type'].upper():8s} | "
                f"{entry['amount']:.8f} BCH | "
                f"TXID: {entry['txid']}"
            )

        print(f"\nSaved to DB — address: {address_to_check}")
        print(f"  Total received : {total_received:.8f} BCH")
        print(f"  Total sent     : {total_sent:.8f} BCH")
        print(f"  Transactions   : {tx_count}")
    
    
