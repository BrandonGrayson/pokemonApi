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

class PokemonCreate(BaseModel):
    name: str
    type: str
    level: int 
    caught: bool
    party: bool
    image: str

    class Config:
        from_attributes = True  

class Pokemon(PokemonCreate):
    owner_id: int    

    class Config:
        from_attributes = True  
        
class PokedexPokemon(PokemonCreate):
    id: int

    class Config:
        from_attributes = True  
