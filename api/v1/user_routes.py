from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.database import get_db
from schemas.userschema import UserCreate, UserResponse, UserUpdate, UserUpdateResponse
from crud.userscrud import create_user, get_user, put_user, patch_user
from core.security import verify_token

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)
""" --- GET ENDPOINTS ---"""

@router.get("/test")
async def test():
    return {"message": "success"}



@router.get("/{username}", response_model=UserResponse)
async def get_user_endpoint(username: str,  db:Session = Depends(get_db),
                            user:dict = Depends(verify_token)):

    user = get_user(username, db)
    return user


""" --- POST ENDPOINTS --- """
@router.post("/", response_model=UserResponse)
async def create_user_endpoint(userschema: UserCreate, db: Session = Depends(get_db)):
    userschema_dict = userschema.model_dump()
    try:
        created_user = create_user(userschema_dict, db)
        return created_user
    except SQLAlchemyError as e:
        return {"message": f"sqlalchemy error\n {e}"}




"""--- EDIT ENDPOINT --- """
@router.put("/edituser/{username}", response_model=UserResponse)
async def edit_user_endpoint(username:str, schema: UserUpdate, db:Session = Depends(get_db),
                             user:str = Depends(verify_token)):
    schema_dict = schema.model_dump()
    user = put_user(username,schema_dict, db)
    return user


@router.patch("/patchuser/{username}", response_model=UserUpdateResponse)
async def patch_user_endpoint(username: str, schema: UserUpdate, db: Session = Depends(get_db),
                              user:str = Depends(verify_token)):
    schema_dict = schema.model_dump()

    user = patch_user(username, schema_dict, db)
    return user



"""--- DELETE ENDPOINT ---"""