from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import uuid

class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

class UserOut(UserBase):
    id: uuid.UUID
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
