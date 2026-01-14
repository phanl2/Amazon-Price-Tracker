import sqlite3
from datetime import datetime

DB_NAME = "prices.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            price REAL NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    conn.commit()
    conn.close()


def get_or_create_product(title: str, url: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM products WHERE url = ?",
        (url,)
    )
    row = cursor.fetchone()

    if row:
        product_id = row[0]
    else:
        cursor.execute(
            "INSERT INTO products (title, url) VALUES (?, ?)",
            (title, url)
        )
        product_id = cursor.lastrowid

    conn.commit()
    conn.close()
    return product_id


def insert_price(product_id: int, price: float):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO prices (product_id, price, timestamp) VALUES (?, ?, ?)",
        (product_id, price, datetime.utcnow().isoformat())
    )

    conn.commit()
    conn.close()
