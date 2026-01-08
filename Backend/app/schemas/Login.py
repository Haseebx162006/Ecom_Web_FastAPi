from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str