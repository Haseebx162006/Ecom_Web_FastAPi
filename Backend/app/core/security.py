from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
pwd_context= CryptContext(schemes=["bcrypt"],deprecated="auto")

def verify_password(plain_password, hash_password):
    pwd_context.verify(plain_password,hash_password)
    
def hash_password(password: str):
    pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode=data.copy()
    
    