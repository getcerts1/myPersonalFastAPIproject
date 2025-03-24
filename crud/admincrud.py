from fastapi import HTTPException, status, Response
from sqlalchemy.orm import Session
from models.usersmodel import Users
from core.security import hash_password




def get_admin_user(username: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user does not exist")

    return user