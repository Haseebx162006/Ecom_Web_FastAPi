from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreateSchema(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class UserReadSchema(BaseModel):
    """Schema for user response"""
    id: int
    email: str
    is_active: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        
class UserUpdateSchema(BaseModel):
    """Schema for updating user"""
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True