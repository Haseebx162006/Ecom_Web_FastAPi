from sqlalchemy import Column, Integer, Boolean, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__= "users"
    id=Column(Integer,primary_key=True, index=True)
    email = Column(String, unique=True)
    hashed_password=Column(String, nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    is_active=Column(Boolean, default=True)
    
    orders=relationship("Orders",back_populates="users",cascade="all,delete")