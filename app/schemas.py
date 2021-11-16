from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):  # can use any name as class name // AND EXTENDING BASE_MODEL
    title: str
    content: str
    published: bool = True  # if the user didn't provide a value post wil automaticaly assign it as True
    """
    rating: Optional[
        int] = None  # this will be a fully optional field. if the user didn't provide a value defuault is set to none
"""


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenDate(BaseModel):
    id: Optional[str] = None


class PostCreate(PostBase):
    pass


class UpdateResponce(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created: datetime

    class Config:
        orm_mode = True


class PostResponce(PostBase):
    id: int
    created: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True
