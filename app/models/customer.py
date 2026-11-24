import sqlite3
from typing import List, Optional

class CustomerModel:

    @staticmethod
    def get_all(conn: sqlite3.Connection) -> List[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, phone FROM customers ORDER BY id DESC")
        return cursor.fetchall()

    @staticmethod
    def create(conn: sqlite3.Connection, name: str, email: Optional[str], phone: Optional[str]) -> int:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customers (name,email, phone) VALUES (?,?,?)", (name,email, phone))
        conn.commit()
        return cursor.lastrowid

    @staticmethod
    def delete(conn: sqlite3.Connection, customer_id: int) -> bool:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        conn.commit()
        return cursor.rowcount > 0