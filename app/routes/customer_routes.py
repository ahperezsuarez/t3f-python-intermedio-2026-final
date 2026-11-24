from fastapi import APIRouter, Depends, status, HTTPException
import sqlite3
from typing import List

from app.database import get_db_connection
from app.models.customer import CustomerModel
from app.views import CustomerCreate, CustomerResponse

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get("/", response_model=List[CustomerResponse])
def get_customers(db: sqlite3.Connection = Depends(get_db_connection)):
    return [dict(r) for r in CustomerModel.get_all(db)]

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(data: CustomerCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    c_id = CustomerModel.create(db, data.name, data.email, data.phone)
    return {**data.model_dump(), "id": c_id}

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    try:
        deleted = CustomerModel.delete(db, customer_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return {"detail": "Cliente eliminado"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="No se puede eliminar un cliente con una venta asociada")