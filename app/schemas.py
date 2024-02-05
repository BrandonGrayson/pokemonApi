from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    userName: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
