import sqlite3

from numpy.core import records


def create_table():
    conn = sqlite3.connect("finans.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    category TEXT,
    date TEXT
    )
        """)

    conn.commit()
    conn.close()

def add_transaction(type_, amount, category):
    conn = sqlite3.connect("finans.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO transactions(type, amount, category, date) VALUES(?,?,?, DATE('now'))",
        (type_, amount, category)
    )

    conn.commit()
    conn.close()

def get_transactions():
    conn = sqlite3.connect("finans.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions")
    data = cursor.fetchall()

    conn.close()
    return data


def delete_transaction(record_id):
    conn = sqlite3.connect("finans.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transactions WHERE id = ?", (record_id,))

    conn.commit()
    conn.close()