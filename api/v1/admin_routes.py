from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from db.database import get_db
from core.security import admin_verify
from crud.admincrud import get_admin_user



router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/{username}")
async def get_admin_user_endpoint(username: str,
                                  db:Session = Depends(get_db),
                                  admin_user: dict = Depends(admin_verify)):
    user = get_admin_user(username, db)
    return {"message":f"welcome {user.username} your role is {user.role}"}
