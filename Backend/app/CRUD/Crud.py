from sqlalchemy.orm import Session
from schemas.Product import Product_Create_Schema, Product_Read_Schema, Product_Update_Schema
from Models.Product import Product
from fastapi import HTTPException, status
from typing import List
from schemas.User import User_Create_Schema
from core.security import hash_password, verify_password
from Models.User import User


def create_Product(db: Session, product: Product_Create_Schema):
	db_product=Product(**product.dict())
	db.add(db_product)
	db.commit()
	db.refresh(db_product)
	return db_product

def delete_product(db:Session, id: int):
    searched_product= db.query(Product).filter(Product.id== id).first()
    
    if not searched_product:
        return {"Error":"Product not found"}
    
    db.delete(Product)
    db.commit()
    
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




def create_user(db:Session, user: User_Create_Schema):
    hashed_pwd= hash_password(user.password)
    
    db_user= User(
        email=user.email,
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
    
