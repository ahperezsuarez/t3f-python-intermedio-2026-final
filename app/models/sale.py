import sqlite3
from typing import List, Dict
from fastapi import HTTPException

class SaleModel:

    @staticmethod
    def create_transaction(conn: sqlite3.Connection, customer_id: int, items: List[Dict]) -> int:
        cursor = conn.cursor()
        try:

            cursor.execute("SELECT id FROM customers WHERE id = ?", (customer_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="cliente no encontrado")

            total_sale = 0.0
            processed_items = []

            for item in items:
                cursor.execute("SELECT name, price, stock FROM products WHERE id = ?", (item["product_id"],))
                prod = cursor.fetchone()
                if not prod:
                    raise HTTPException(status_code=404, detail=f"Producto {item['product_id']} no existe")
                if prod["stock"] < item["quantity"]:
                    raise HTTPException(status_code=400, detail=f"Stock insuficiente para: {prod['name']}")

                subtotal = prod["price"] * item["quantity"]
                total_sale += subtotal
                processed_items.append({
                    "product_id": item["product_id"],
                    "quantity": item["quantity"],
                    "unit_price": prod["price"],
                    "subtotal": subtotal
                }) 

            cursor.execute("INSERT INTO sales (customer_id, total) VALUES (?,?)", (customer_id, total_sale))
            sale_id = cursor.lastrowid

            for p_item in processed_items:
                cursor.execute("""
                
                INSERT INTO sale_details(sale_id, product_id,quantity,unit_price, subtotal) VALUES (?,?,?,?,?)

                """, (sale_id,p_item["product_id"],p_item["quantity"],p_item["unit_price"],p_item["subtotal"]))

                cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (p_item["quantity"],p_item["product_id"]))

            conn.commit()
            return sale_id
        except Exception:
            conn.rollback()
            raise

    @staticmethod
    def get_all(conn: sqlite3.Connection) -> List[dict]:
            cursor = conn.cursor()
            cursor.execute("""
            
            SELECT s.id, s.customer_id, c.name as customer_name, s.date, s.total
            FROM sales s
            JOIN customers c ON s.customer_id = c.id
            ORDER BY s.id DESC
            """)

            sales = [dict(row) for row in cursor.fetchall()]

            for s in sales:
                cursor.execute("""

                SELECT sd.id, sd.product_id, p.name as product_name, sd.quantity, sd.unit_price, sd.subtotal
                FROM sale_details sd
                JOIN products p ON sd.product_id = p.id
                WHERE sd.sale_id = ?

                """, (s["id"],))
                s["items"] = [dict(d) for d in cursor.fetchall()]

            return sales
