from django.db import models

class Definition(models.Model):
    def __init__(self, short_def: str, long_def: str = None, context_def: str = None):
        self.short_def = short_def
        self.long_def = long_def
        self.context_def = context_def

    def get_short_def(self):
        return self.short_def

    def get_long_def(self):
        if self.long_def:
            return self.long_def
        else:
            return self.short_def

    def get_context_def(self):
        if self.context_def:
            return self.context_def
        else:
            return self.short_def

    def add_context_def(self, definition: str):
        if self.context_def is None:
            self.context_def = definition
        else:
            self.context_def += definition