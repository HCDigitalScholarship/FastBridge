from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()

class AtlasClient ():
    
    def __init__ (self, altas_uri, dbname):
        self.mongodb_client = MongoClient(altas_uri, tls=True, tlsAllowInvalidHostnames=True, tlsAllowInvalidCertificates=True)
        self.database = self.mongodb_client[dbname]

    ## A quick way to test if we can connect to Atlas instance
    def ping (self):
        self.mongodb_client.admin.command('ping')

    def get_collection (self, collection_name):
        collection = self.database[collection_name]
        return collection
    
    def find (self, collection_name, filter = {}, limit=0):
        collection = self.database[collection_name]
        items = list(collection.find(filter=filter, limit=limit))
        return items

    def get_database(self, dbname):
        selected_database = self.mongodb_client[dbname]
        return selected_database

try: 
    DB_NAME = 'Latin-Texts'
    ATLAS_URI = os.getenv('ATLAS_URI')

    atlas_client = AtlasClient (ATLAS_URI, DB_NAME)
    atlas_client.ping()
    print('Connected to Atlas instance! We are good to go!!')
    db = atlas_client.database
    dict_db = atlas_client.get_database('dictionaries')

except ConnectionFailure as e:
    print(f"Failed to connect to MongoDB: {e}")
    raise
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    raise




