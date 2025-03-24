from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.database import get_db
from models.usersmodel import Users
from core.security import create_token, verify_password
from schemas.token import Token


router = APIRouter(
    prefix="/user",
    tags=["Authentication"]
)

@router.post("/login", response_model=Token)
async def login(login_schema: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == login_schema.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with email {login_schema.username} not found")

    if not verify_password(login_schema.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    if user.role == "user":

        created_token = create_token({
            "user_id": user.id,
            "time_created": int(user.time_created.timestamp()),  # convert datetime to int timestamp
            "role": "user"
        })

    elif user.role == "admin":
        created_token = create_token({
            "admin_id": user.id,
            "time_created": int(user.time_created.timestamp()),  # convert datetime to int timestamp
            "role": "admin"
        })


    return {"access_token": created_token, "token_type": "bearer"}