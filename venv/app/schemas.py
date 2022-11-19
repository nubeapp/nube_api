from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class TmpCodeBase(BaseModel):
    email: str
    code: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    username: str
    name: str
    country: str
    phone: str
    firstSurname: Optional[str] = None
    secondSurname: Optional[str] = None

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserResponse(UserBase):
    created_at: datetime

    class Config:
        orm_mode = True


class UserLoginEmail(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
