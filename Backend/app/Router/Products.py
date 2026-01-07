from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from app.schemas.Product import Product_Create_Schema, Product_Read_Schema, Product_Update_Schema
from app.CRUD.Crud import create_Product, get_all_products, update_Product, delete_product
from app.Models.Product import Product
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/products",
    tags=["Products"]
)


@router.post("/", response_model=Product_Read_Schema, status_code=status.HTTP_201_CREATED)
def create_product(product: Product_Create_Schema, db: Session = Depends(get_db)):
    """Create a new product"""
    return create_Product(db, product)


@router.get("/", response_model=list[Product_Read_Schema])
def list_products(db: Session = Depends(get_db)):
    """Get all products"""
    return get_all_products(db)


@router.get("/{product_id}", response_model=Product_Read_Schema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a product by ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    return product


@router.put("/{product_id}", response_model=Product_Read_Schema)
def update_product(product_id: int, product_update: Product_Update_Schema, db: Session = Depends(get_db)):
    """Update a product"""
    return update_Product(db, product_update, product_id)


@router.delete("/{product_id}")
def remove_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product"""
    return delete_product(db, product_id)
