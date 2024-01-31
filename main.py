from typing import Union
from pydantic import BaseModel

from fastapi import FastAPI

class User(BaseModel):
    userName: str
    password: str

app = FastAPI()


@app.post("/createUser")
def createUser(user: User):
    return user