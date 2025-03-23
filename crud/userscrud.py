from db.database import get_db
from fastapi import HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from models.usersmodel import Users
from core.security import hash_password, verify_password



def create_user(userschema, db: Session):

    check_user_exists = db.query(Users).filter(Users.password == userschema["username"]).first()
    if check_user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user already exists")

    userschema["password"] = hash_password(userschema["password"])
    new_user = Users(**userschema)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_user(email: str, db: Session):
    check_user_exists = db.query(Users).filter(Users.username == email).first()

    if not check_user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user does not exist")

    return check_user_exists

def edited_user(username, updated_schema, db: Session):
    #compare user provided password to db passwords, if the same continue as normal, if different
    #hash new password
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    hashed_pass = hash_password(updated_schema["password"])
    updated_schema["password"] = hashed_pass

    updated_user = Users(**updated_schema)
    db.add(updated_user)
    db.commit()
    db.refresh(updated_user)

    return updated_user





