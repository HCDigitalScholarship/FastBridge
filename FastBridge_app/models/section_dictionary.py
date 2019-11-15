from FastBridge_app.models.i_dictionary import IDictionary
from FastBridge_app.models.definition import Definition
from django.db import models

class SectionDictionary(IDictionary):
    def __init__(self, language: str, title: str, section: str):
        self.title = title
        self.section = section
        super().__init__(language)

    def add_word(self, word: str, definition: Definition):
        if self.dict.get(word) is None:
            self