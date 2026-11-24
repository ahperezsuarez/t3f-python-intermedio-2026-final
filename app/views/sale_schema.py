from pydantic import BaseModel , Field
from typing import List

class SaleDetailCreate(BaseModel):
    product_id: int = Field(...,gt=0)
    quantity: int = Field(...,gt=0)

class SaleCreate(BaseModel):
    customer_id: int = Field(...,gt=0)
    items: List[SaleDetailCreate] = Field(..., min_length=1)

class SaleDetailResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float

    class Config:
        from_attributes = True

class SaleResponse(BaseModel):
    id: int
    customer_id: int
    customer_name: str
    date: str
    total: float
    items: List[SaleDetailResponse] = []

    class Config:
        from_attributes = True