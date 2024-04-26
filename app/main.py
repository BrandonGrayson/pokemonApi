from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schemas, models, crud, oauth2, database, utils
from .database import engine
from sqlalchemy import select, update

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

@app.post("/login/",  response_model=schemas.Token)
def loginUser(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    print('user cred', user_credentials)
    user = db.query(models.Users).filter(models.Users.username == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify_password(user_credentials.password, user.password):
        print(user_credentials.password)
        print(user.password)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    print('access token --->', access_token)

    return {"access_token" : access_token, "token_type": "bearer"} 

@app.post("/addPokemon", status_code=status.HTTP_201_CREATED, response_model=schemas.Pokemon)
def addPokemon(pokemon_credentials: schemas.PokemonCreate,  db: Session = Depends(database.get_db), user_id: int = Depends(oauth2.get_current_user)):

    if not user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You Are Not Signed In.")
    
    new_pokemon = models.Pokemon(owner_id=user_id, **pokemon_credentials.dict())
    db.add(new_pokemon)
    db.commit()
    db.refresh(new_pokemon)

    return new_pokemon

# route for getting all a users pokemon
@app.get("/getAllPokemon", status_code=status.HTTP_200_OK, response_model=list[schemas.PokedexPokemon])
def getUserPokemon(user_id: int = Depends(oauth2.get_current_user)):

    session = Session(engine)

    if not user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You Are Not Signed In.")
    
    all_pokemon = select(models.Pokemon).where(models.Pokemon.owner_id == user_id)

    pokemon = session.scalars(all_pokemon).all()
    
    return pokemon

@app.put('/updatePokemon/{id}', status_code=status.HTTP_200_OK)
def updateUserPokemon(id: str, pokemon: schemas.PokemonCreate, user_id: int = Depends(oauth2.get_current_user)):
    
    session = Session(engine)

    print('id', id)

    if not user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You Are Not Signed In.")
    
    session.execute(update(models.Pokemon).where(models.Pokemon.id == id).values({"name": pokemon.name, "type": pokemon.type, "level": pokemon.level, "caught": pokemon.caught, "party": pokemon.party, "image": pokemon.image}))

    session.commit()

    post_query = select(models.Pokemon).where(models.Pokemon.id == id)

    pokemon_update = session.scalars(post_query).first()

    print('pokemon', pokemon_update)

    return pokemon_update


