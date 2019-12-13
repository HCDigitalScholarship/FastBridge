from django.db import models

from FastBridge_app.models.definition import Definition
from FastBridge_app.models.master_dictionary import MasterDictionary

# TODO: Figure out propagation of changes in definitions from master_dict to book_dict and vice versa. And settle definitions from books
class IRepository():
    def __init__(self, language: str):
        self.master_dict = MasterDictionary(language)
        self.book_dict = dict()

    async def get_word_from_master_dict(self, word: str):
        return self.master_dict.get_word(word)

    async def get_all_words_from_master_dict(self):
        return self.master_dict.get_all_definitions()

    async def add_word_to_master_dict(self, word: str, definition: dict):
        short_def = definition.get("short_def") if definition.get("short_def") is not None else None
        if short_def is None:
            raise ValueError("Definition must at least have a short definition")
        final_def = Definition(short_def, definition.get("long_def"), definition.get("context_def"))
        self.master_dict.add_word(word, final_def)
        return {word: definition}

    async def delete_word_from_master_dict(self, word: str):
        if self.master_dict.dict.get(word) is not None:
            self.master_dict.delete_word(word)

    async def get_all_words_from_book_dict(self):
        pass

    async def add_word_to_book_dict(self, word: str):
        pass

    async def delete_word_from_book_dict(self, word: str):
        pass