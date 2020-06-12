#backend for users loging in and creating accounts. Based on the tutorial starting here: https://fastapi.tiangolo.com/tutorial/security/
from typing import Optional
from fastapi import FastAPI, WebSocket, Request, File, Form, UploadFile, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from datetime import datetime, timedelta
from jwt import PyJWTError
from passlib.context import CryptContext
import jwt
from typing import List
from sqlalchemy.orm import Session
from sql_app import crud, models, schema
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
#app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


SECRET_KEY = "369cce7237dd24ebbbe8ba3c9ea4ce7568e63862383395c931b559c96dc1279c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)






oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def authenticate_user(db : Session, username: str, password: str):
    user = crud.get_user_by_username(db, username)
    if not user:
        print("wrong username")
        return False
    if not verify_password(password, user.hashed_password):
        print("wrong password")
        return False
    return user

def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt






@app.get("/users/", response_model=List[schema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users





@app.post("/users/{user_id}/texts/", response_model=schema.Text)
def create_text_for_user(
    user_id: int, text: schema.TextCreate, sections : str, db: Session = Depends(get_db)
):
    return crud.create_user_text(db=db, text=text, sections = sections, user_id=user_id)


@app.get("/texts/", response_model=List[schema.Text])
def read_texts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    texts = crud.get_texts(db, skip=skip, limit=limit)
    return texts


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)

    if user is None:
        raise credentials_exception
    user.disabled = False
    return user


async def get_current_active_user(current_user: schema.User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schema.User)
async def read_users_me(current_user: schema.User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/{username}", response_model=schema.User)
def read_user(username: str, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_active_user)):
    db_user = crud.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
