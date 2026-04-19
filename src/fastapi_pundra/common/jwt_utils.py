from datetime import datetime, timedelta, UTC
from jose import jwt

# Default values for development, but should be overridden in production
SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 525600  # 1 year (365 days * 24 hours * 60 minutes)
REFRESH_TOKEN_EXPIRE_DAYS = 730      # 2 years

def create_access_token(data: dict, expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES, algorithm: str = ALGORITHM, secret_key: str = SECRET_KEY):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)

def create_refresh_token(data: dict, expire_days: int = REFRESH_TOKEN_EXPIRE_DAYS, algorithm: str = ALGORITHM, secret_key: str = SECRET_KEY):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=expire_days)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)

def decode_token(token: str, algorithm: str = ALGORITHM, secret_key: str = SECRET_KEY, options: dict = None) -> dict:
    """
    Decode and verify a JWT token
    Returns the decoded payload if valid, raises JWTError if invalid
    """
    if not token:
        raise jwt.JWTError("Token is missing")
        
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=[algorithm], options=options)
        return decoded_token
    except jwt.JWTError as e:
        raise jwt.JWTError(f"Invalid token: {str(e)}")