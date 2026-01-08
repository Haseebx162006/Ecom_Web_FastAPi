from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from app.dependencies import get_current_user
from app.Models.User import User
from app.CRUD.Crud import create_order, get_user_orders, get_order_by_id, update_order_status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List

router = APIRouter(
    prefix="/api/orders",
    tags=["Orders"]
)


class OrderItemInput(BaseModel):
    product_id: int = None
    productId: int = None  # Support frontend format
    quantity: int = Field(gt=0)
    
    def get_product_id(self):
        """Get product_id from either field"""
        return self.product_id or self.productId


class CreateOrderRequest(BaseModel):
    items: List[OrderItemInput]


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_order(
    order_data: CreateOrderRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new order"""
    # Convert to backend format
    items = []
    for item in order_data.items:
        product_id = item.get_product_id()
        if product_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="product_id or productId is required"
            )
        items.append({"product_id": product_id, "quantity": item.quantity})
    
    return create_order(db, current_user.id, items)


@router.get("/")
def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all orders for the current user"""
    return get_user_orders(db, current_user.id)


@router.get("/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific order"""
    order = get_order_by_id(db, order_id)
    
    # Check if order belongs to the current user
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this order"
        )
    
    return order


@router.put("/{order_id}/status")
def update_status(
    order_id: int,
    status_update: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update order status (admin only)"""
    order = get_order_by_id(db, order_id)
    
    # Check if order belongs to the current user
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this order"
        )
    
    return update_order_status(db, order_id, status_update.get("status"))
