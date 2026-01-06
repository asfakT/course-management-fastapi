from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, HttpUrl

# Pydantic Model (Request Body)
class CourseCreate(BaseModel):
    name: str
    instructor: str
    duration: int
    website: HttpUrl

class CourseResponse(CourseCreate):
    id : int
    creator_id : int
    class Config:
        orm_mode = True


#spesific field show
# class CourseResponse(BaseModel):
#     name: str
#     instructor: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRes(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[int] = None