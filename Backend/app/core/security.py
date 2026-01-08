from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt

# Configure argon2 as the password hashing algorithm
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__time_cost=2,
    argon2__memory_cost=65536,
    argon2__parallelism=1
)

# JWT Configuration
SECRET_KEY = "your-secret-key-change-this-to-a-strong-random-string"  # Change this to a strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    """
    Hash a password using argon2.
    
    Args:
        password: Plain text password from user
        
    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    Truncates the plain password to 72 bytes for compatibility.
    
    Args:
        plain_password: Plain text password from user login
        hashed_password: Hashed password from database
        
    Returns:
        True if passwords match, False otherwise
    """
    try:
        # Truncate to 72 bytes for compatibility
        truncated_pwd = plain_password[:72]
        return pwd_context.verify(truncated_pwd, hashed_password)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None, expire_time: Optional[timedelta] = None):
    """
    Create a JWT access token.
    
    Args:
        data: Data to encode in the token
        expires_delta: Optional expiration time delta
        expire_time: Optional expiration time delta (alternative parameter name)
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    # Use expire_time if provided, otherwise use expires_delta
    delta = expire_time if expire_time else expires_delta
    
    if delta:
        expire = datetime.utcnow() + delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt