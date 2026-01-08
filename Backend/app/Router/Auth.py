# app/Router/Auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
import traceback

try:
    from ..Models import User
    from database import get_db
    from app.schemas.User import UserCreateSchema, UserReadSchema
    from app.schemas.Login import UserLogin
    from app.core.security import create_access_token, hash_password, verify_password
except ImportError as e:
    print(f"Import error in Auth.py: {e}")
    raise

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreateSchema, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        print(f"Register attempt: email={user.email}")
        print(f"Password received: {len(user.password)} characters")
        
        # Check existing user
        print("Checking for existing user...")
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            print("User already exists")
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash password
        print(f"About to hash password...")
        try:
            hashed_pwd = hash_password(user.password)
            print(f"Password hashed successfully, length={len(hashed_pwd)}")
        except Exception as hash_err:
            print(f"Hash error: {hash_err}")
            print(traceback.format_exc())
            raise hash_err

        # Create new user
        print(f"Creating user in database...")
        new_user = User(email=user.email, hashed_password=hashed_pwd)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"User created successfully: {new_user.id}")
        
        return {
            "id": new_user.id,
            "email": new_user.email,
            "is_active": new_user.is_active,
            "created_at": new_user.created_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Registration error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login user and return access token"""
    try:
        # Find user by email
        user_obj = db.query(User).filter(User.email == user.email).first()
        
        if not user_obj or not verify_password(user.password, user_obj.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        access_token = create_access_token(
            data={"sub": str(user_obj.id)},
            expire_time=timedelta(minutes=30)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user_obj.id,
            "email": user_obj.email
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Login failed")

