from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from app.Router import Auth, Products, Orders, Cart
import sqlalchemy

# Create tables
try:
    Base.metadata.create_all(bind=engine)
    
    # Try to add missing columns for existing databases
    try:
        db_url = str(engine.url).lower()
        
        if 'sqlite' in db_url:
            # SQLite migration
            with engine.connect() as conn:
                result = conn.execute(sqlalchemy.text("PRAGMA table_info(products)"))
                columns = [row[1] for row in result]
                
                if 'featured' not in columns:
                    conn.execute(sqlalchemy.text("ALTER TABLE products ADD COLUMN featured BOOLEAN DEFAULT 0"))
                    conn.commit()
                
                if 'image_url' not in columns:
                    conn.execute(sqlalchemy.text("ALTER TABLE products ADD COLUMN image_url VARCHAR(500)"))
                    conn.commit()
        elif 'postgresql' in db_url or 'postgres' in db_url:
            # PostgreSQL migration - use begin() for proper transaction handling
            with engine.begin() as conn:
                # Check if columns exist
                check_query = sqlalchemy.text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='products' AND column_name IN ('featured', 'image_url')
                """)
                result = conn.execute(check_query)
                existing_columns = [row[0] for row in result]
                
                if 'featured' not in existing_columns:
                    print("Adding 'featured' column to products table (PostgreSQL)...")
                    conn.execute(sqlalchemy.text("ALTER TABLE products ADD COLUMN featured BOOLEAN DEFAULT FALSE"))
                    print("✓ Added 'featured' column")
                else:
                    print("✓ 'featured' column already exists")
                
                if 'image_url' not in existing_columns:
                    print("Adding 'image_url' column to products table (PostgreSQL)...")
                    conn.execute(sqlalchemy.text("ALTER TABLE products ADD COLUMN image_url VARCHAR(500)"))
                    print("✓ Added 'image_url' column")
                else:
                    print("✓ 'image_url' column already exists")
    except Exception as e:
        print(f"Note: Could not migrate existing database (this is OK if tables are new): {e}")
        import traceback
        traceback.print_exc()
except Exception as e:
    print(f"Error creating tables: {e}")
    import traceback
    traceback.print_exc()

app = FastAPI(
    title="E-commerce API",
    description="E-commerce backend API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(Auth.router)
app.include_router(Products.router)
app.include_router(Orders.router)
app.include_router(Cart.router)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to E-commerce API",
        "docs": "/docs",
        "openapi_schema": "/openapi.json"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
