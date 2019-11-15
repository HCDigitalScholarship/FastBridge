from django.db import models
from abc import ABC, abstractmethod

# Create your models here.

class IDictionary(ABC):
    def __init__(self, language:str):
        self.language = language
        self.dict = dict()

    @abstractmethod
    def add_word(self, word:str, definition:str):
        pass

    @abstractmethod
    def delete_word(self, word:str):
        pass