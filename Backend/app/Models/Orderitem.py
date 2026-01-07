from sqlalchemy import Column, Integer, Boolean, String, DateTime, ForeignKey,Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    
    order_id = Column(Integer, ForeignKey("Orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)  
    
    order = relationship("Orders", back_populates="items")
    product = relationship("Product", back_populates="order_items")