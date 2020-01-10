from django.db import models
import datetime
from django.db import models

# Create your models here.

class IDictionary(models.Model):
    def __init__(self, language: str):
        self.language = language
        self.last_updated = datetime.datetime.now()
        self.dict = dict()

    class Meta:
        abstract = True