import sqlite3
from typing import List, Optional

class ProductModel:

    @staticmethod
    def get_all(conn: sqlite3.Connection) -> List[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, stock FROM products ORDER BY id DESC")
        return cursor.fetchall()

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, product_id: int) -> Optional[sqlite3.Row]:
        cursor = conn.cursor() 
        cursor.execute("SELECT id, name, price, stock FROM products WHERE id = ?",(product_id,))
        return cursor.fetchone()

    @staticmethod
    def create(conn: sqlite3.Connection, name: str, price: float, stock: int) -> int:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name,price, stock) VALUES (?,?,?)", (name,price, stock))
        conn.commit()
        return cursor.lastrowid

    @staticmethod
    def update(conn: sqlite3.Connection,product_id:int ,name: str, price: float, stock: int) -> bool:
            cursor = conn.cursor()
            cursor.execute("UPDATE products SET name = ?, price = ?, stock = ? WHERE id = ?", (name,price, stock, product_id))
            conn.commit()
            return cursor.rowcount > 0
    
    @staticmethod
    def delete(conn: sqlite3.Connection, product_id: int) -> bool:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        return cursor.rowcount > 0