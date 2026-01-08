from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile, Form
from database import get_db
from app.schemas.Product import Product_Create_Schema, Product_Read_Schema, Product_Update_Schema
from app.CRUD.Crud import create_Product, get_all_products, update_Product, delete_product
from app.Models.Product import Product
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter(
    prefix="/api/products",
    tags=["Products"]
)


@router.post("", response_model=Product_Read_Schema, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=Product_Read_Schema, status_code=status.HTTP_201_CREATED)
async def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    image_url: Optional[str] = Form(None),
    featured: Optional[str] = Form("false"),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Create a new product (supports both JSON and FormData)"""
    try:
        # Convert featured string to boolean
        featured_bool = False
        if featured:
            if isinstance(featured, str):
                featured_bool = featured.lower() in ("true", "1", "yes")
            else:
                featured_bool = bool(featured)
        
        # If image file is provided, use a placeholder URL (in production, upload to cloud storage)
        if image:
            # For now, just use the image_url if provided, or a placeholder
            if not image_url:
                image_url = f"https://via.placeholder.com/400x400?text={name.replace(' ', '+')}"
        
        product_data = Product_Create_Schema(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            image_url=image_url,
            featured=featured_bool
        )
        return create_Product(db, product_data)
    except Exception as e:
        import traceback
        print(f"Error in create_product: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating product: {str(e)}"
        )


@router.get("", response_model=list[Product_Read_Schema])
@router.get("/", response_model=list[Product_Read_Schema])
def list_products(
    featured: Optional[str] = Query(None, description="Filter by featured products (true/false)"),
    db: Session = Depends(get_db)
):
    """Get all products, optionally filtered by featured"""
    try:
        products = get_all_products(db)
        
        # Handle featured filter - convert string to boolean if needed
        if featured is not None:
            # Convert string "true"/"false" to boolean
            if isinstance(featured, str):
                featured_bool = featured.lower() in ("true", "1", "yes")
            else:
                featured_bool = bool(featured)
            
            # Filter products, handling None values (existing products without featured field)
            filtered_products = []
            for p in products:
                # Safely get featured attribute, default to False if not present or None
                product_featured = False
                try:
                    product_featured = getattr(p, 'featured', False)
                    if product_featured is None:
                        product_featured = False
                except (AttributeError, KeyError):
                    product_featured = False
                
                if product_featured == featured_bool:
                    filtered_products.append(p)
            products = filtered_products
        
        # Convert products to schema, handling missing attributes
        result = []
        for p in products:
            try:
                product_dict = {
                    'id': p.id,
                    'name': p.name,
                    'description': p.description,
                    'quantity': p.quantity,
                    'price': p.price,
                    'image_url': getattr(p, 'image_url', None),
                    'featured': getattr(p, 'featured', False) or False
                }
                result.append(Product_Read_Schema(**product_dict))
            except Exception as e:
                print(f"Error serializing product {p.id}: {e}")
                # Skip products that can't be serialized
                continue
        
        return result
    except Exception as e:
        import traceback
        print(f"Error in list_products: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching products: {str(e)}"
        )


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
