from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from app.Router import Auth, Products, Orders, Login

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(

)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #  frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(Auth.router)
app.include_router(Products.router)
app.include_router(Orders.router)
app.include_router(Login.router)


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
