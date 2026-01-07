from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from app.schemas.Login import UserLogin
from app.CRUD.Crud import authenticate_user
from app.core.security import create_access_token
from datetime import timedelta  
router= APIRouter(
    prefix="/Router/Login",
    tags=["Login"]
)

@router.post("/login")
def Login(user: UserLogin, db= Depends(get_db)):
    user= authenticate_user(db,user.username, user.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    
    access_token=create_access_token(
        data={"sub":str(user.id)},
        expire_time= timedelta(minutes=30)
    )
    
    return {"access_token": access_token,"token_type":"bearer"}
