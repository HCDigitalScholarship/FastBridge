import datetime

from FastBridge_app.models.i_dictionary import IDictionary
from FastBridge_app.models.definition import Definition
from FastBridge_app.models.section import Section
from django.db import models

class SectionDictionary(IDictionary):
    def __init__(self, language: str, title: str, section: Section):
        self.title = title
        self.section = section
        super().__init__(language)

    def get_word(self, word: str):
        value = self.dict.get(word)
        if value:
            return Definition(value["short_def"], value["long_def"], value["context_def"])
        else:
            raise ValueError("%s does not exist in %s" % (word, self.section.get_section_as_string()))

    def add_word(self, word: str, definition: Definition):
        value = self.dict
        value[word] = definition
        self.last_updated = datetime.datetime.now()

    def delete_word(self, word: str):
        del self.dict[word]
        self.last_updated = datetime.datetime.now()