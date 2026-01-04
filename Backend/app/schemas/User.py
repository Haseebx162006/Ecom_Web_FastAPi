from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Create (input from frontend)
class UserCreateSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr 
    password: str = Field(..., min_length=6)

# Read (response to frontend)
class UserReadSchema(BaseModel):
    id: int 
    username: str
    name: str
    email: str

    class Config:
        from_attributes = True  

class UserUpdateSchema(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
