#functions for accessing the database. If we move texts fully into the database, rewrite DefinitionTools.py in here. I personally find the python files I created more intuitive and easier to manage than a database. clangen 6/8/2020
from sqlalchemy.orm import Session

from . import models, schema

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_texts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Text).offset(skip).limit(limit).all()

def create_user(db: Session, user: schema.UserCreate):
    hashed_password = get_password_hash(user.password)
    if user.username == "admin" or user.username == "clangen":
        db_user = models.User(username=user.username, hashed_password=hashed_password, add_access = True)
    else:
        db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_text(db: Session, title : str):
    return db.query(models.Text).filter(models.Text.title == title).first()

def create_user_text(db: Session, text: schema.TextCreate, title: str, sections : str, user_id: int):
    db_text = models.Text(**text.dict(), owner_id=user_id, sections =  sections)
    db.add(db_text)
    db.commit()
    db.refresh(db_text)
    return db_text
