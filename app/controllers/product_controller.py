import sqlite3
from fastapi import HTTPException, status
from app.models.product import ProductModel
from app.views import ProductCreate, ProductUpdate

class ProductController:

    @staticmethod
    def list_products(conn: sqlite3.Connection):
        rows = ProductModel.get_all(conn)
        return [dict(row) for row in rows]

    @staticmethod
    def get_product(conn: sqlite3.Connection, product_id: int):
        row = ProductModel.get_by_id(conn, product_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {product_id} no se encuentra."
            )
        return dict(row)

    @staticmethod
    def create_product(conn: sqlite3.Connection, date: ProductCreate):
        new_id = ProductModel.create(conn, date.name ,date.price ,date.stock)
        return{**date.model_dump(), "id": new_id}

    @staticmethod
    def update_product(conn: sqlite3.Connection, product_id: int ,date: ProductUpdate):
        update = ProductModel.update(conn, product_id, date.name, date.price, date.stock)
        if not update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {product_id} no se encuentra."
            )
        return {**date.model_dump(), "id": product_id}

    @staticmethod
    def delete_product(conn: sqlite3.Connection, product_id: int):
        delete = ProductModel.delete(conn, product_id)
        if not delete:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Producto con ID {product_id} no se encuentra."
                    )
        return {"detail": "Producto eliminado exitosamente"}