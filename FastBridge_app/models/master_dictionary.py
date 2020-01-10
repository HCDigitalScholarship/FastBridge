from FastBridge_app.models.i_dictionary import IDictionary
from FastBridge_app.models.definition import Definition
from django.db import models

class MasterDictionary(IDictionary):
    def __init__(self, language:str):
        super().__init__(language)

    def get_all_definitions(self):
        return self.dict

    def get_word(self, word: str):
        value = self.dict.get(word)
        if value:
            return Definition(value["short_def"], value["long_def"])
        else:
            raise ValueError("%s does not exist in master dictionary")

    def add_word(self,  word: str, definition: Definition):
        if self.dict.get(word) is None:
            self.dict[word] = {"short_def": definition.get_short_def(), "long_def": definition.get_long_def()}
        else:
            self.dict[word]["short_def"] = definition.get_short_def()
            self.dict[word]["long_def"] = definition.get_long_def()

    def delete_word(self, word: str):
        del self.dict[word]
