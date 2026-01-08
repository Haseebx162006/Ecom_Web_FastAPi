from pydantic import BaseModel
from typing import Optional
from typing import List
from datetime import datetime
from .OrderItem import Create_OrderItem_Schema, Read_OrderItem_Schema, Update_OrderItem_Schema
class Create_Order_Schema(BaseModel):
    user_id: int
    items: List[Create_OrderItem_Schema]
    
class Read_order_Schema(BaseModel):
    user_id: int
    order_id: int 
    items:List[Read_OrderItem_Schema]
    price: float
    created_at: datetime
    class Config:
        from_attributes=True
    
class Update_order_Schema(BaseModel):
    items:Optional[List[Update_OrderItem_Schema]]=None