from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.database import get_db
from schemas.userschema import UserCreate, UserResponse, UserUpdate, UserUpdateResponse
from crud.userscrud import create_user, get_user, edited_user



router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.get("/test")
async def test():
    return {"message": "success"}

@router.post("/", response_model=UserResponse)
async def create_user_endpoint(userschema: UserCreate, db: Session = Depends(get_db)):
    userschema_dict = userschema.model_dump()
    try:
        created_user = create_user(userschema_dict, db)
        return created_user
    except SQLAlchemyError as e:
        return {"message": f"sqlalchemy error\n {e}"}


@router.get("/{username}", response_model=UserResponse)
async def get_user_endpoint(username: str, db:Session = Depends(get_db)):

    user = get_user(username, db)
    return user


@router.put("/edituser/{username}", response_model=UserResponse)
async def edit_user_endpoint(username:str, schema: UserUpdate, db:Session = Depends(get_db)):
    schema_dict = schema.model_dump()
    user = edited_user(username,schema_dict, db)
    return user


@router.patch("/patchuser/{username}")
async def patch_user_endpoint():
    pass