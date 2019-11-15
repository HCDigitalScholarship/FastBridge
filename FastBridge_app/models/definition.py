from django.db import models

class Definition(models.Model):
    def __init__(self, short_def: str, long_def: str=None, context_def: str = None):
        self._short_def = short_def
        self._long_def = long_def
        self._context_def = context_def

    def get_short_def(self):
        return self._short_def

    def get_long_def(self):
        if self._long_def:
            return self._long_def
        else:
            return self._short_def

    def get_context_def(self):
        if self._context_def:
            return self._context_def
        else:
            return self._short_def
