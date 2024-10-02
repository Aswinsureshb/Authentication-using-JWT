# jwt key
import datetime
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta, timezone
from typing import Optional

JWT_SECRET_KEY = "123412341234123412341234"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRY_SECONDS = 10
ACCESS_TOKEN_EXPIRY_MINUTES = 2

    
def create_access_token(payload: dict, expires_delta: Optional[timedelta]=None):
    # make sure there is an expiry
    if expires_delta:
        expire = datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=5)
    payload.update({"exp": expire})
    encoded_jwt = jwt.encode(payload, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def get_current_user(jwtoken):
    try:
        decoded_jwt = jwt.decode(jwtoken, JWT_SECRET_KEY, ALGORITHM )
        userid = decoded_jwt["username"]
        return userid
    except jwt.PyJWTError:
        return {}
    
def is_jwt_valid(jwtoken):
    try:
        decoded_jwt = jwt.decode(jwtoken, JWT_SECRET_KEY, ALGORITHM )
        return True
    except PyJWTError:
        return False
