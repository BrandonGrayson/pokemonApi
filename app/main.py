from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schemas, models, crud, oauth2, database, utils
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

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

@app.post("/createUser/", response_model=schemas.User)
def createUser(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    
    hashed_password = utils.pwd_context.hash(user.password)
    user.password = hashed_password
    return crud.create_user(db=db, user=user)

@app.post("/login/",  )
def loginUser(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.username == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token" : access_token, "token_type": "bearer"} 

# Send a query to the Users table with the user info sent from the body of the route
# Verify that the credentials being sent from the route match whats inside the db
# if user exists 
