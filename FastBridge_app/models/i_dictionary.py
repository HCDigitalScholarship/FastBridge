from django.db import models
import datetime
from abc import ABC, abstractmethod

# Create your models here.

class IDictionary(ABC):
    def __init__(self, language: str):
        self.language = language
        self.last_updated = datetime.datetime.now()
        self.dict = dict()

    @abstractmethod
    def add_word(self, word:str, definition:str):
        pass

    @abstractmethod
    def delete_word(self, word:str):
        pass