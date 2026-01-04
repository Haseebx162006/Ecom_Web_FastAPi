from pydantic import BaseModel, Field
from typing import Optional

class Create_OrderItem_Schema(BaseModel):
    product_id: int 
    quantity: int = Field(gt=0)
class Read_OrderItem_Schema(BaseModel):
    product_id: int 
    quantity: int = Field(gt=0)
    price:float
class Update_OrderItem_Schema(BaseModel):
    quantity: Optional[int] = Field(gt=0)