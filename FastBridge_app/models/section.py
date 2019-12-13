from django.db import models

class Section(models.Model):
    def __init__(self, section_number: int, chapter_number: int, book_number: int):
        self.section_number = section_number
        self.chapter_number = chapter_number
        self.book_number = book_number

    def get_section_as_string(self):
        return self.book_number + "." + self.chapter_number + "." + self.section_number

    def get_section_from_string(self, section_string: str):
        section_substring = section_string.split(".")
        self.book_number = section_substring[0]
        self.chapter_number = section_substring[1]
        self.section_number = section_substring[2]
        return self

    def is_larger_than_compared_section(self, input):
        if self.book_number > input.book_number:
            return True
        elif self.book_number < input.book_number:
            return False
        else:
            if self.chapter_number > input.chapter_number:
                return True
            elif self.chapter_number < input.chapter_number:
                return False
            else:
                if self.section_number > input.section_number:
                    return True
                elif self.section_number < input.section_number:
                    return False
                else:
                    raise ValueError("Comparing same sections of the same book")