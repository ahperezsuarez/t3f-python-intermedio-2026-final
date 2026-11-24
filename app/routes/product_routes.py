from fastapi import APIRouter, Depends, status
import sqlite3
from typing import List

from app.database import get_db_connection
from app.controllers.product_controller import ProductController
from app.views import ProductResponse, ProductCreate , ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductResponse])
def get_products(db: sqlite3.Connection = Depends(get_db_connection)):
    return ProductController.list_products(db)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return ProductController.get_product(db, product_id)

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    return ProductController.create_product(db, product)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: sqlite3.Connection = Depends(get_db_connection)):
    return ProductController.update_product(db, product_id, product)

@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(product_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return ProductController.delete_product(db, product_id)