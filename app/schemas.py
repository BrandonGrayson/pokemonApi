from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str | None = None

class UserLogin(BaseModel):
    username: str
    password: str

class IncomingPokemonCredentials(BaseModel):
    name: str
    type: str
    level: int
    caught: bool
    inParty: bool
    
class Pokemon(IncomingPokemonCredentials):
    user_id: int