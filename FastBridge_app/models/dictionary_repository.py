from FastBridge_app.models.i_repository import IRepository
from django.db import models

class DictionaryRepository(IRepository):
    def __init__(self, database=dict()):
        super().__init__(database)

    async def create_data(self, input):
        pass

    async def read_data(self, input):
        pass

    async def update_data(self, input):
        pass

    async def delete_data(self, input):
        pass