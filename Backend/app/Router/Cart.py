from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from app.dependencies import get_current_user
from app.Models.User import User
from app.Models.Order import Orders
from app.Models.Orderitem import OrderItem
from app.Models.Product import Product
from app.schemas.Cart import Add_to_Cart_Schema
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/cart",
    tags=["Cart"]
)


def get_or_create_cart(db: Session, user_id: int) -> Orders:
    """Get user's pending cart (order with status 'Cart') or create a new one"""
    cart = db.query(Orders).filter(
        Orders.user_id == user_id,
        Orders.status == "Cart"
    ).first()
    
    if not cart:
        cart = Orders(user_id=user_id, status="Cart", total_price=0.0)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    return cart


@router.get("")
@router.get("/")
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's cart"""
    cart = get_or_create_cart(db, current_user.id)
    
    # Get cart items with product details
    items = db.query(OrderItem).filter(OrderItem.order_id == cart.id).all()
    
    cart_items = []
    total_price = 0.0
    
    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            item_data = {
                "id": item.id,
                "product_id": item.product_id,
                "name": product.name,
                "description": product.description,
                "price": item.price,
                "quantity": item.quantity,
                "image": product.image_url or "https://via.placeholder.com/400x400?text=Product"
            }
            cart_items.append(item_data)
            total_price += item.price * item.quantity
    
    return {
        "id": cart.id,
        "items": cart_items,
        "total_price": total_price,
        "created_at": cart.created_at
    }


@router.post("/items")
def add_to_cart(
    item: Add_to_Cart_Schema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add item to cart"""
    # Get or create cart
    cart = get_or_create_cart(db, current_user.id)
    
    # Check if product exists
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {item.product_id} not found"
        )
    
    # Check if item already exists in cart
    existing_item = db.query(OrderItem).filter(
        OrderItem.order_id == cart.id,
        OrderItem.product_id == item.product_id
    ).first()
    
    if existing_item:
        # Update quantity
        existing_item.quantity += item.quantity
        if existing_item.quantity > product.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock"
            )
    else:
        # Create new cart item
        if item.quantity > product.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock"
            )
        existing_item = OrderItem(
            order_id=cart.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price
        )
        db.add(existing_item)
    
    # Update cart total
    cart.total_price = sum(
        item.price * item.quantity 
        for item in db.query(OrderItem).filter(OrderItem.order_id == cart.id).all()
    )
    
    db.commit()
    db.refresh(existing_item)
    
    return {
        "id": existing_item.id,
        "product_id": existing_item.product_id,
        "quantity": existing_item.quantity,
        "price": existing_item.price
    }


class UpdateCartItemRequest(BaseModel):
    quantity: int = Field(gt=0)


@router.put("/items/{item_id}")
def update_cart_item(
    item_id: int,
    request: UpdateCartItemRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update cart item quantity"""
    quantity = request.quantity
    if quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than 0"
        )
    
    # Get cart
    cart = get_or_create_cart(db, current_user.id)
    
    # Get cart item
    cart_item = db.query(OrderItem).filter(
        OrderItem.id == item_id,
        OrderItem.order_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    # Check product stock
    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if quantity > product.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock"
        )
    
    # Update quantity
    cart_item.quantity = quantity
    
    # Update cart total
    cart.total_price = sum(
        item.price * item.quantity 
        for item in db.query(OrderItem).filter(OrderItem.order_id == cart.id).all()
    )
    
    db.commit()
    db.refresh(cart_item)
    
    return {
        "id": cart_item.id,
        "product_id": cart_item.product_id,
        "quantity": cart_item.quantity,
        "price": cart_item.price
    }


@router.delete("/items/{item_id}")
def remove_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove item from cart"""
    # Get cart
    cart = get_or_create_cart(db, current_user.id)
    
    # Get cart item
    cart_item = db.query(OrderItem).filter(
        OrderItem.id == item_id,
        OrderItem.order_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    db.delete(cart_item)
    
    # Update cart total
    remaining_items = db.query(OrderItem).filter(OrderItem.order_id == cart.id).all()
    if remaining_items:
        cart.total_price = sum(item.price * item.quantity for item in remaining_items)
    else:
        cart.total_price = 0.0
    
    db.commit()
    
    return {"message": "Item removed from cart"}


@router.delete("")
@router.delete("/")
def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Clear all items from cart"""
    cart = get_or_create_cart(db, current_user.id)
    
    # Delete all cart items
    db.query(OrderItem).filter(OrderItem.order_id == cart.id).delete()
    cart.total_price = 0.0
    
    db.commit()
    
    return {"message": "Cart cleared"}

