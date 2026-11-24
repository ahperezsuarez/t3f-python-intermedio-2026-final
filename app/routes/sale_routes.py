from fastapi import APIRouter, Depends, status
import sqlite3
from typing import List

from app.database import get_db_connection
from app.models.sale import SaleModel
from app.views import SaleCreate, SaleResponse

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.get("/", response_model=List[SaleResponse])
def get_sales(db: sqlite3.Connection = Depends(get_db_connection)):
    return SaleModel.get_all(db)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_sale(data: SaleCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    items_dicts = [i.model_dump() for i in data.items]
    sale_id = SaleModel.create_transaction(db, data.customer_id, items_dicts)
    return {"message": "Venta procesada exitosamente", "sale_id": sale_id}