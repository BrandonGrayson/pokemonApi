from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from . import schemas, models

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/createUser")
def createUser(user: schemas.UserBase):
    return user