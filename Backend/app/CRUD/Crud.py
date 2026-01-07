from sqlalchemy.orm import Session
from app.schemas.Product import Product_Create_Schema, Product_Read_Schema, Product_Update_Schema
from app.Models.Product import Product
from fastapi import HTTPException, status
from typing import List
from app.schemas.User import UserCreateSchema
from app.core.security import hash_password, verify_password
from app.Models.User import User


def create_Product(db: Session, product: Product_Create_Schema):
	db_product=Product(**product.dict())
	db.add(db_product)
	db.commit()
	db.refresh(db_product)
	return db_product

def delete_product(db: Session, id: int):
    # fetch the product instance
    searched_product = db.query(Product).filter(Product.id == id).first()
    
    if not searched_product:
        return {"Error": "Product not found"}
    
    # delete the instance, not the class
    db.delete(searched_product)
    db.commit()
    
    return {"Success": f"Product with id {id} deleted"}

    
def update_Product(db:Session, new_product: Product_Update_Schema, id: int):
    product= db.query(Product).filter(Product.id==id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found"
        )
        
    if new_product.name is not None:
        product.name = new_product.name
    if new_product.quantity is not None:
        product.quantity = new_product.quantity
    if new_product.price is not None:
        product.price = new_product.price

    db.commit()
    db.refresh(product)  # Refresh to get updated data
    return product


def get_all_products(db: Session):
    return db.query(Product).all()




def create_user(db:Session, user: UserCreateSchema):
    hashed_pwd= hash_password(user.password)
    
    db_user= User(
        username=user.username,
        hashed_password=hashed_pwd
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db:Session,username:str, password:str):
    user= db.query(User).filter(User.username==username).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
    return user


# ==================== Order Functions ====================

def create_order(db: Session, user_id: int, items: List[dict]):
    """Create a new order"""
    from app.Models.Order import Orders
    from Models.Orderitem import OrderItem
    
    if not items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must contain at least one item"
        )
    
    # Calculate total price
    total_price = 0
    for item in items:
        product = db.query(Product).filter(Product.id == item["product_id"]).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item['product_id']} not found"
            )
        if product.quantity < item["quantity"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product {product.name}"
            )
        total_price += product.price * item["quantity"]
    
    # Create order
    db_order = Orders(user_id=user_id, total_price=total_price)
    db.add(db_order)
    db.flush()  # Flush to get order ID
    
    # Add order items
    for item in items:
        product = db.query(Product).filter(Product.id == item["product_id"]).first()
        order_item = OrderItem(
            order_id=db_order.id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            price=product.price
        )
        db.add(order_item)
        # Decrease product quantity
        product.quantity -= item["quantity"]
    
    db.commit()
    db.refresh(db_order)
    return db_order


def get_user_orders(db: Session, user_id: int):
    """Get all orders for a user"""
    from app.Models.Order import Orders
    
    return db.query(Orders).filter(Orders.user_id == user_id).all()


def get_order_by_id(db: Session, order_id: int):
    """Get a specific order"""
    from app.Models.Order import Orders
    
    order = db.query(Orders).filter(Orders.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order


def update_order_status(db: Session, order_id: int, status: str):
    """Update order status"""
    from app.Models.Order import Orders
    
    order = db.query(Orders).filter(Orders.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    valid_statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {valid_statuses}"
        )
    
    order.status = status
    db.commit()
    db.refresh(order)
    return order
