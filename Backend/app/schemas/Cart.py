from fastapi import HTTPException, status
from pydantic import BaseModel, Field
from app.schemas.OrderItem import Read_OrderItem_Schema
from typing import List
from datetime import datetime
class Add_to_Cart_Schema(BaseModel):
    product_id: int
    quantity: int =Field(gt=0)
class Read_Cart_Schema(BaseModel):
     id: int                  # order_id
     items: List[Read_OrderItem_Schema]
     total_price: float
     created_at: datetime

     class Config:
        from_attributes = True
    