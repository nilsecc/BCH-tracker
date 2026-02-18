import sqlite3
from src.database.database import DB_NAME


def _query(sql, params=()):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    return rows


def address_summary(address):
    rows = _query("SELECT total_received, total_sent, tx_count FROM addresses WHERE address=?", (address,))
    if not rows:
        print(f"Address {address} not found in DB.")
        return
    received, sent, tx_count = rows[0]
    balance = received - sent
    ratio = (sent / received * 100) if received else 0
    print(f"\n── Address summary: {address}")
    print(f"   Total received : {received:.8f} BCH")
    print(f"   Total sent     : {sent:.8f} BCH")
    print(f"   Net balance    : {balance:.8f} BCH")
    print(f"   Spent ratio    : {ratio:.1f}%")
    print(f"   Transactions   : {tx_count}")


def tx_stats(address):
    for tx_type in ('received', 'sent'):
        rows = _query(
            "SELECT amount FROM transactions WHERE address=? AND type=?",
            (address, tx_type)
        )
        if not rows:
            continue
        amounts = [r[0] for r in rows]
        print(f"\n── {tx_type.capitalize()} tx stats ({len(amounts)} txs)")
        print(f"   Max    : {max(amounts):.8f} BCH")
        print(f"   Min    : {min(amounts):.8f} BCH")
        print(f"   Avg    : {sum(amounts)/len(amounts):.8f} BCH")


def activity_by_block(address):
    rows = _query(
        "SELECT block_height, COUNT(*) FROM transactions WHERE address=? GROUP BY block_height ORDER BY block_height DESC",
        (address,)
    )
    if not rows:
        print("No transactions found.")
        return
    print(f"\n── Activity by block")
    for block_height, count in rows:
        print(f"   Block {block_height}: {count} tx(s)")


def print_all(address):
    address_summary(address)
    tx_stats(address)
    activity_by_block(address)
