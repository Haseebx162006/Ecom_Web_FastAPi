from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
pwd_context= CryptContext(schemes=["bcrypt"],deprecated="auto")
from config import ALGORITHM , ACCESS_TOKEN_EXPIRE, SECRET_KEY

def verify_password(plain_password, hash_password):
    pwd_context.verify(plain_password,hash_password)
    
def hash_password(password: str):
    pwd_context.hash(password)


def create_access_token(data: dict, expire_time:timedelta):
    to_encode=data.copy()
    if expire_time:
        expire=datetime.utcnow()+expire_time
    else:
        expire=datetime.utcnow()+timedelta(minutes=30)
        
    to_encode.update({
        
        "exp":expire
    })
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    