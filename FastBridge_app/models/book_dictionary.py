import datetime

from FastBridge_app.models.i_dictionary import IDictionary
from FastBridge_app.models.definition import Definition
from FastBridge_app.models.section import Section
from FastBridge_app.models.section_dictionary import SectionDictionary
from typing import List
from django.db import models

class BookDictionary(IDictionary, models.Model):
    def __init__(self, language:str, title:str, sections: List[SectionDictionary]):
        self.title = title
        self.dict = self.convert_input_section_dicts_into_dict_of_section_dicts(sections)
        super().__init__(language)

    def convert_input_section_dicts_into_dict_of_section_dicts(self, sections: List[SectionDictionary]):
        dict_of_section_dicts = dict()
        for section in sections:
            dict_of_section_dicts[section.section.get_section_as_string()] = section
        return dict_of_section_dicts

    def get_word_from_section(self, word: str, section: Section):
        section_dict = self.dict.get(section.get_section_as_string())
        return section_dict.get_word(word)

    def get_word_from_selected_sections(self, word: str, sections: List[Section]):
        definition = Definition()
        for section in sections:
            section_definition = self.get_word_from_section(word, section)
            definition.short_def = section_definition.short_def
            definition.long_def = section_definition.long_def
            definition.add_context_def(section_definition.context_def)
        return definition

    def get_words_from_section(self, section: Section):
        return self.dict.get(section.get_section_as_string())

    def get_words_from_sections(self, sections: List[Section]):
        definitions = dict()
        for section in sections:
            section_dict = self.dict.get(section.get_section_as_string()).dict
            for key, value in section_dict.items():
                if definitions.get(key) is not None:
                    definitions[key].add_context_def(value.context_def)
                else:
                    definitions[key] = value
        return definitions

    def add_word(self, word: str, section: Section, definition: Definition):
        section_dict = self.dict.get(section.get_section_as_string())
        section_dict.add_word(word, definition)
        self.last_updated = datetime.datetime.now()

    def replace_with_updated_dict(self, sections: List[SectionDictionary]):
        dict_of_new_section_dicts = self.convert_input_section_dicts_into_dict_of_section_dicts(sections)
        for key, value in dict_of_new_section_dicts.items():
            self.dict[key] = value
        self.last_updated = datetime.datetime.now()

    def delete_word(self, word: str):
        del self.dict[word]
        self.last_updated = datetime.datetime.now()
