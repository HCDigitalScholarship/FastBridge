#based on this https://medium.com/data-rebels/fastapi-how-to-add-basic-and-cookie-authentication-a45c85ef47d3
#and this Based on the tutorial starting here: https://fastapi.tiangolo.com/tutorial/security/
#The medium article fills in the missing pieces of the official tutorial

from typing import Optional, List
import base64
from passlib.context import CryptContext
from datetime import datetime, timedelta

import jwt
from jwt import PyJWTError

from pydantic import BaseModel
from fastapi import APIRouter, WebSocket, Request, File, Form, UploadFile, Depends, HTTPException, status

from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm, OAuth2, OAuth2PasswordBearer
from fastapi.security.base import SecurityBase
from fastapi.openapi.models import SecurityBase as SecurityBaseModel
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.utils import get_openapi

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, Response, JSONResponse
from starlette.requests import Request

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

from sqlalchemy.orm import Session
from . import crud, models, schema #database interaction stuff. This should be from . import, but that complained
from .database import SessionLocal, engine #more database interaction stuff. Technially, this should be from .database, but this complains for unknown reasons
import add_new_text
import importlib
import DefinitionTools

models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()
templates = Jinja2Templates(directory="templates")
router_path = Path.cwd()


SECRET_KEY = "67f5a5fa48fdf258937c065e7cc0f89a8f0e17ac4f2603d28079a66b7911d728"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 *24




class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)





class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        header_authorization: str = request.headers.get("Authorization")
        cookie_authorization: str = request.cookies.get("Authorization")
        print(header_authorization, " header auth recieved")
        print(cookie_authorization, " cookie auth recieved")
        header_scheme, header_param = get_authorization_scheme_param(
            header_authorization
        )
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization
        )
        if header_scheme.lower() == "bearer":
            authorization = True
            scheme = header_scheme
            param = header_param

        elif cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme
            param = cookie_param

        else:
            authorization = False

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        return param


class BasicAuth(SecurityBase):
    def __init__(self, scheme_name: str = None, auto_error: bool = True):
        self.scheme_name = scheme_name or self.__class__.__name__
        self.model = SecurityBaseModel(type= "http")
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "basic":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        print(param, "param")
        return param
basic_auth = BasicAuth(auto_error=False)
oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="/token")

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
        expire = datetime.utcnow() + timedelta(minutes=60*24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
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

@router.get("/users/", response_model=List[schema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.post("/update_my_words/")
def create_text_for_user( request : Request, title: str = Form(...), language: str = Form(...), start : str = Form(...), end: str = Form(...), db: Session = Depends(get_db),
current_user: schema.User = Depends(get_current_user)):
    print(title)
    print(language)
    sections = f"{start} - {end}"
    text = schema.TextCreate(title = title, language= language)
    crud.create_user_text(db=db, title = title, text=text, sections = sections, user_id=current_user.id)
    context = {}
    context['request'] = request
    context['welcome'] = f'You told us that you know {title}: {sections}'
    return templates.TemplateResponse("account_management.html", context)

"""
#debugging to see texts in db – restrict to admin or delete for production
@router.get("/texts/", response_model=List[schema.Text])
def read_texts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    texts = crud.get_texts(db, skip=skip, limit=limit)
    return texts
"""



async def get_current_active_user(current_user: schema.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive User",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user

@router.post("/token", response_model=Token)
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
    user.is_active = True
    return Token(access_token = access_token, token_type= "bearer")



@router.post("/login")
@router.get("/login")
async def login_basic(auth: BasicAuth = Depends(basic_auth), db: Session = Depends(get_db)):
    print(auth)
    if not auth:
        response = Response(headers={"WWW-Authenticate": "Basic"}, status_code=401)
        return response

    try:
        decoded = base64.b64decode(auth).decode("ascii")
        username, _, password = decoded.partition(":")
        user = authenticate_user(db, username, password)
        print("authenticated")
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        print("got user")

        access_token_expires = timedelta(minutes=60*24)
        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        print("made access token")
        token = jsonable_encoder(access_token)
        print(token)
        response = RedirectResponse(url="/account/manage/")
        response.set_cookie(
            "Authorization",
            value=f"Bearer {token}",
            httponly=True,
            max_age=60*60*24,

        )
        return response

    except:
        response = Response(headers={"WWW-Authenticate": "Basic"}, status_code=401)
        return response

@router.get("/logout/")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie("Authorization")
    return response


@router.get("/docs")
async def get_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

@router.get("/addwords")
async def import_words(request : Request, current_user: schema.User = Depends(get_current_active_user)):
    context = {"request" : request}
    #this one will take a csv of titles and the information we care about for them, and add it to the right dictionay when submitted.
    return templates.TemplateResponse("import-words.html", context)

@router.get("/signup/")
def signup_handler(request: Request):
    context = {"request" : request}
    return templates.TemplateResponse("signup.html", context)




@router.post("/signup/")
def create_user(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    context = {"request" : request}
    user = schema.UserCreate(username = username, password = password)
    #print(db)
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    crud.create_user(db, user)
    response =  RedirectResponse(url="/account/login/")
    return response

@router.get("/import")
async def import_index(request : Request, current_user: schema.User = Depends(get_current_user)):
    context = {"request" : request}
    print(current_user)
    if current_user == None or not current_user.add_access:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only some accounts may add texts")

    #this html form will take a csv of a lemmatized text, a number of expected subsections, and a language as input.
    return templates.TemplateResponse("import.html", context)

@router.get("/delete")
async def delete_index(request : Request, current_user: schema.User = Depends(get_current_user)):
    context = {"request" : request}
    print(current_user)
    if current_user == None or not current_user.add_access:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only some accounts may delete texts")

    #this html form will take a csv of a lemmatized text, a number of expected subsections, and a language as input.
    return templates.TemplateResponse("delete.html", context)


@router.get("/current_texts")
async def view_texts(request : Request):
    """This will need to be updated manually when new languages are added"""
    context = {"request" : request}
    context['latin'] =  ['Latin texts:'] +  list(importlib.import_module(f'data.Latin.texts').texts)
    context['greek'] = ['Greek texts:']+ list(importlib.import_module(f'data.Greek.texts').texts) #uncomment once Greek is added
    return templates.TemplateResponse("current_texts.html", context)

@router.post("/import/handler/")
async def import_handler(request : Request, file: UploadFile = File(...), title : str = Form(...), language : str = Form(...), subsections : int = Form(...), local_def : str = Form(...), local_lem : str = Form(...), current_user: schema.User = Depends(get_current_active_user)):
    local_def = local_def == "Yes"
    local_lem = local_lem == "Yes"
    context = {"request" : request}
    context["link_back"] ="/account/import"
    to_return = add_new_text.import_(title, subsections, file, language, local_def, local_lem)
    if to_return == "added a text":
        context["result"] = "Successful upload!!!"
        context["next_action"] = "add another"
    else:
        context["result"] = f"{to_return}\nFailed to upload"
        context["next_action"] = "try again"

    return templates.TemplateResponse("upload_result.html", context)
@router.post("/addingwords/")
async def import_words(file: UploadFile = File(...), language : str = Form(...), current_user: schema.User = Depends(get_current_active_user)):
    return add_new_text.add_words(file.file, language)

@router.post("/delete/handler/")
async def delete_handler(request : Request, title : str = Form(...), language : str = Form(...), local_def : str = Form(...), local_lem : str = Form(...), current_user: schema.User = Depends(get_current_active_user)):
    local_def = local_def == "Yes"
    local_lem = local_lem == "Yes"
    context = {"request" : request}
    context["link_back"] ="/account/delete"
    to_return = add_new_text.delete_(title, language, local_def, local_lem)
    if to_return == "deleted a text":
        context["result"] = "Successful delete!!!"
        context["next_action"] = "delete another"
    else:
        context["result"] = f"{to_return}\nFailed to delete"
        context["next_action"] = "try again"

    return templates.TemplateResponse("upload_result.html", context)

@router.post("/manage/")
@router.get("/manage/")
async def welcome(request : Request, user : schema.User = Depends(get_current_active_user)):
    context = {"request" : request}
    context["welcome"] = f"Welcome {user.username}"
    latin= DefinitionTools.render_titles("Latin")
    greek= DefinitionTools.render_titles("Greek")#uncomment once Greek is added
    context["texts"] = latin + greek
    return templates.TemplateResponse("account_management.html", context)


@router.get("/search/")
async def choose_select_or_oracle(request: Request):
    context= {"request" : request}
    latin= DefinitionTools.render_titles("Latin")
    greek= DefinitionTools.render_titles("Greek")#uncomment once Greek is added
    context["texts"] = latin + greek
    return templates.TemplateResponse("giant_form.html", context)

@router.post("/my_known_words/")
async def user_operation_with_known_words(user : schema.User = Depends(get_current_active_user), lang : str =  Form(...), function : str = Form(...), other_texts : str = Form(...), starts: Optional[str] = Form(""), ends: Optional[str] = Form(""), in_exclue : Optional[str] = Form(''), section_depth : Optional[str] = Form([])):
    """
    user: I think this really is the user. I hope. Then we can just do user.read_texts to get the first set of triples, and reformat them into the url.
    Function: select or oracle
    other texts: the texts to explore in oracle, or the ones being read for select (should be triplable)
    conditional on what they choose for function:
    if select:
        starts: the list of start sections for those texts
        ends: ditto but ends
        in_exclude: just what it is in the select function
    if oracle:
        section_depth: how large of sections they want

    Based on what we have, we will make the url for the search
    """
    my_texts = [text for text in user.read_texts if text.language == lang]
    print(my_texts)
    #we can force the user to always enter a start and end section when entering texts in account management; it will make this step much, much simpler and be clearer to them when they update sections they have read. Otherwise, everything with triple[1] needs to be in a try/except block with in the for loop, which is quite messy, especially since we don't have a good marker for the end of a text yet... maybe I should add that to the importer actually.
    known_text_url = ""
    url_starts = ""
    url_ends = ""
    for triple in my_texts:
        known_text_url+= triple.title.lower().replace(",", "").replace(" ", "_")+"+"
        start, part, end = triple.sections.partition("-")
        print(start)
        url_starts+= start.strip() +"+"
        url_ends+= end.strip() +"+"
    search_url_start=  f"/{function}/{lang}/result/"
    search_url_end = f"{known_text_url}/{url_starts[:-1]}-{url_ends[:-1]}/"
    search_url_mid = f""
    for text in other_texts.split(";"): #we need a clear expectation about what character divides texts. commas could be problematic because of author, work conventions, but it seems more natural than a semicolon... need to consult with Bret before finalizing.
        to_add = text.lower().replace(",", "").replace(" ", "_")
        print(to_add)
        search_url_mid += f"{to_add}+"
        print(search_url_mid)
    search_url_mid= search_url_mid[:-1] #remove the final extra "+"
    if(function == "oracle"):
        starts= starts.replace(",", "+")
        ends= ends.replace(",", "+")
        search_url_mid+=f"/{starts}/{ends}"
        search_url_mid+= f"/{section_depth}/"

    elif(function == "select"):
        starts= starts.replace(",", "+")
        ends= ends.replace(",", "+")
        search_url_mid+=f"/{starts}-{ends}"
        search_url_mid+= f"/{in_exclue}/"
        search_url_end+="non_running/"
    else:
        return{"That is not a valid function"}
    search_url = search_url_start+search_url_mid+search_url_end
    return RedirectResponse(search_url)

#End of user management code
