from FastBridge_app.models.i_dictionary import IDictionary
from FastBridge_app.models.definition import Definition
from django.db import models

class BookDictionary(IDictionary, models.Model):
    def __init__(self, language:str, title:str):
        self.title = title
        super().__init__(language)

    def add_word(self,  word: str, section: str, definition: Definition):
        if self.dict.get(word) is None:
            self.dict[word] = {"short_def": definition.get_short_def(), "long_def": definition.get_long_def()
                               , "context_def": {section: definition.get_context_def()}}
        else:
            self.dict[word]["short_def"] = definition.get_short_def()
            self.dict[word]["long_def"] = definition.get_long_def()
            self.dict[word]["context_def"][section] = definition.get_context_def()

    def delete_word(self, word: str):
        del self.dict[word]
