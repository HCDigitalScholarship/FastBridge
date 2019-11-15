from django.db import models
from abc import ABC, abstractmethod

# Create your models here.

class IRepository(ABC):
    def __init__(self, database=dict()):
        self.database = database

    @abstractmethod
    def create_data(self, input):
        pass

    @abstractmethod
    def read_data(self, input):
        pass

    @abstractmethod
    def update_data(self, input):
        pass

    @abstractmethod
    def delete_data(self, input):
        pass