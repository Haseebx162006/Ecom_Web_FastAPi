from sqlalchemy import Column, Integer, Boolean, String, DateTime, ForeignKey
from sqlalchemy.orm import Relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __table__= "users"
    id=Column(Integer,primary_key=True, index=True)
    username=Column(String(50),unique=True, nullable=False)
    hashed_password=Column(String,unique=True, nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    is_active=Column(Boolean, default=True)
    
    orders=Relationship("Orders",back_populates="users",cascade="all,delete")