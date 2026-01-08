from sqlalchemy.orm import Session
from app.schemas.Product import Product_Create_Schema, Product_Read_Schema, Product_Update_Schema
from app.schemas.User import UserCreateSchema
from app.Models.Product import Product
from app.Models.User import User
from app.core.security import hash_password, verify_password
from fastapi import HTTPException, status
from typing import List


# ==================== PRODUCT FUNCTIONS ====================

def create_Product(db: Session, product: Product_Create_Schema):
    """Create a new product"""
    try:
        db_product = Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating product: {str(e)}"
        )


def get_all_products(db: Session):
    """Get all products"""
    try:
        return db.query(Product).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching products: {str(e)}"
        )


def get_product_by_id(db: Session, product_id: int):
    """Get a specific product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    return product


def update_Product(db: Session, new_product: Product_Update_Schema, id: int):
    """Update an existing product"""
    product = db.query(Product).filter(Product.id == id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found"
        )
    
    try:
        if new_product.name is not None:
            product.name = new_product.name
        if new_product.description is not None:
            product.description = new_product.description
        if new_product.quantity is not None:
            product.quantity = new_product.quantity
        if new_product.price is not None:
            product.price = new_product.price

        db.commit()
        db.refresh(product)
        return product
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating product: {str(e)}"
        )


def delete_product(db: Session, id: int):
    """Delete a product"""
    try:
        searched_product = db.query(Product).filter(Product.id == id).first()
        
        if not searched_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {id} not found"
            )
        
        db.delete(searched_product)
        db.commit()
        
        return {"message": f"Product with id {id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting product: {str(e)}"
        )


# ==================== USER FUNCTIONS ====================

def create_user(db: Session, user: UserCreateSchema):
    """Create a new user with hashed password"""
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        hashed_pwd = hash_password(user.password)
        
        db_user = User(
            email=user.email,
            hashed_password=hashed_pwd
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


def authenticate_user(db: Session, email: str, password: str):
    """Authenticate user by email and password"""
    try:
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        return user
    except Exception as e:
        print(f"Error authenticating user: {str(e)}")
        return None


def get_user_by_id(db: Session, user_id: int):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user


def get_user_by_email(db: Session, email: str):
    """Get user by email"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found"
        )
    return user


# ==================== ORDER FUNCTIONS ====================

def create_order(db: Session, user_id: int, items: List[dict]):
    """Create a new order with items"""
    try:
        from app.Models.Order import Orders
        from app.Models.orderitem import OrderItem  # lowercase
        
        if not items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order must contain at least one item"
            )
        
        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        
        # Calculate total price and validate items
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
        db_order = Orders(user_id=user_id, total_price=total_price, status="Pending")
        db.add(db_order)
        db.flush()
        
        # Add order items and update product quantities
        for item in items:
            product = db.query(Product).filter(Product.id == item["product_id"]).first()
            order_item = OrderItem(
                order_id=db_order.id,
                product_id=item["product_id"],
                quantity=item["quantity"],
                price=product.price
            )
            db.add(order_item)
            product.quantity -= item["quantity"]
        
        db.commit()
        db.refresh(db_order)
        return db_order
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating order: {str(e)}"
        )


def get_user_orders(db: Session, user_id: int):
    """Get all orders for a user"""
    try:
        from app.Models.Order import Orders
        orders = db.query(Orders).filter(Orders.user_id == user_id).all()
        return orders if orders else []
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching orders: {str(e)}"
        )


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


def get_all_orders(db: Session):
    """Get all orders (admin function)"""
    try:
        from app.Models.Order import Orders
        return db.query(Orders).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching orders: {str(e)}"
        )


def update_order_status(db: Session, order_id: int, new_status: str):
    """Update order status"""
    from app.Models.Order import Orders
    order = db.query(Orders).filter(Orders.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    valid_statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    try:
        order.status = new_status
        db.commit()
        db.refresh(order)
        return order
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating order: {str(e)}"
        )


def delete_order(db: Session, order_id: int):
    """Delete an order and its items"""
    try:
        from app.Models.Order import Orders
        from app.Models.orderitem import OrderItem  # lowercase
        
        order = db.query(Orders).filter(Orders.id == order_id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Delete order items first
        db.query(OrderItem).filter(OrderItem.order_id == order_id).delete()
        
        # Delete order
        db.delete(order)
        db.commit()
        
        return {"message": f"Order {order_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting order: {str(e)}"
        )