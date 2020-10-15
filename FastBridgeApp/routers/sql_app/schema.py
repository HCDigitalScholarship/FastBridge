from typing import List

from pydantic import BaseModel

class TextBase(BaseModel):
    title: str
    language: str



class TextCreate(TextBase):
    pass


class Text(TextBase):
    sections : str
    owner_id : int
    class Config:
        orm_mode = True




class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    #susbclass for creating users; protects the password


class User(UserBase):
    #
    id: int
    is_active: bool
    read_texts: List[Text] = []
    add_access: bool
    class Config:
        orm_mode = True
