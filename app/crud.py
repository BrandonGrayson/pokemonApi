from sqlalchemy.orm import Session
from . import models, schemas

def create_user(db: Session, user: schemas.UserBase):
    db_user = models.Users(username = user.username, password = user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()
