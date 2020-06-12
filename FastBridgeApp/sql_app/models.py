"""Models for the database tables. Column(Type) just defines the type we expect that column to contain, rather than acually assigning a value to it."""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    no_add_access = Column(Boolean, default=True)
    read_texts =  relationship("Text", back_populates="owner")



class Text(Base):
    __tablename__ = "texts"
    title = Column(String, primary_key=True, index=True)
    sections = Column(String) #these are just the sections that the user has read, not all sections in the text. Those are stored in the file system.
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="read_texts")
