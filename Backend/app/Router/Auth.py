from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from app.schemas.User import UserCreateSchema, UserReadSchema
from app.schemas.Login import UserLogin
from app.CRUD.Crud import create_user, authenticate_user
from app.core.security import create_access_token
from sqlalchemy.orm import Session
from datetime import timedelta

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED)
def register(user: UserCreateSchema, db: Session = Depends(get_db)):
    """Register a new user"""
    from app.Models.User import User
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    return create_user(db, user)


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login user and return access token"""
    user_obj = authenticate_user(db, user.username, user.password)
    
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(
        data={"sub": str(user_obj.id)},
        expire_time=timedelta(minutes=30)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user_obj.id,
        "username": user_obj.username
    }
