from sqlalchemy import Column, Integer, Boolean, String, DateTime, ForeignKey,Float
from sqlalchemy.orm import Relationship
from sqlalchemy.sql import func
from database import Base

class Orders(Base):
    __table__="Orders"
    id=Column(Integer,primary_key=True, index=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    created_at= Column(DateTime(timezone=True),server_default=func.now())
    updated_at= Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
    status=Column(String,default="Pending")
    total_price=Column(Float,nullable=False)
    items = Relationship("OrderItem", back_populates="order", cascade="all, delete")
    users=Relationship("User", back_populates="orders")
    