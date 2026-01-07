from sqlalchemy import Column, Integer, Boolean, String, DateTime, ForeignKey,Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(150), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    order_items = relationship(
        "OrderItem",
        back_populates="product"
    )