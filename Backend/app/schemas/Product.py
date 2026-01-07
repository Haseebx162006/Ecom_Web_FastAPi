from pydantic import BaseModel, Field
from typing import Optional

class Product_Read_Schema(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=150)
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)
    
    class Config:
        from_attributes = True

class Product_Create_Schema(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=150)
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)
    
class Product_Update_Schema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=150)
    quantity: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, gt=0)
