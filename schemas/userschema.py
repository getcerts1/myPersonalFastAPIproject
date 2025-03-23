from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

from typing_extensions import Optional


class UserCreate(BaseModel):
    username: EmailStr
    password: str

    class Config:
        from_attributes = True



class UserResponse(BaseModel):
    id: int
    username: str
    time_created: datetime
    message: Optional[str] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

    class Config:
        from_attribute = True

class UserUpdateResponse(BaseModel):
    id: int
    username: Optional[str] = None
    password: Optional[str] = None

    class Config:
        from_attribute = True