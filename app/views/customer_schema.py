from pydantic import BaseModel , Field
from typing import Optional

class CustomerBase(BaseModel):
    name:str = Field(...,min_length=1,max_length=150)
    email: Optional[str] = Field(None,max_length=150)
    phone: Optional[str] = Field(None,max_length=50)

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int
    
    class Config:
        from_attributes = True