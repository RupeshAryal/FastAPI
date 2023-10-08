from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(BaseModel):
    title: str
    content: str
    published: bool

    class Config:
        orm_model = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_model = True


class UserLogin(BaseModel):
    email: EmailStr

class Token(BaseModel):
    access_token: str
    toke_type: str

class TokenData(BaseModel):
    id: Optional[str] = None




