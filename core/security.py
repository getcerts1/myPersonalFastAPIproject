from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from core.config import ALGORITHM, SECRET, EXPIRATION_TIME
from datetime import datetime, timedelta


password_context = CryptContext(schemes="bcrypt")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
#this line is responsible for extracting tokens


def hash_password(password: str):
    new_pass = password_context.hash(password)
    return new_pass


def verify_password(old_password: str, new_password: str):
    return password_context.verify(old_password, new_password)



"""
creating a token requires a payload for integrity, algorithm and signature
"""


def create_token(payload: dict):
    payload_copy = payload.copy()
    now = datetime.now()
    expiration = now + timedelta(minutes=EXPIRATION_TIME)

    payload_copy.update({
        "exp": int(expiration.timestamp()),
        "iat": int(now.timestamp())
    })

    token = jwt.encode(payload_copy, SECRET, algorithm=ALGORITHM)
    return token


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])

        if not payload.get("user_id") or not payload.get("role"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Malformed payload")

        return payload

    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid or expired token: {e}")



def admin_verify(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        role = payload.get("role")

        if role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admins only")

        return payload


    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid or expired token: {e}")

