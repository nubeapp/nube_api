from datetime import datetime
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
    firstSurname: str
    secondSurname: str
    country: str
    phone: str


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserResponse(UserBase):
    created_at: datetime

    class Config:
        orm_mode = True
