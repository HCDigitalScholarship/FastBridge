from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()

class AtlasClient ():
    
    def __init__ (self, altas_uri, dbname, tls=True):
        # TLS is required by Atlas but breaks against a plain local/CI Mongo, so it is
        # toggleable. Default True keeps production behavior unchanged.
        if tls:
            self.mongodb_client = MongoClient(altas_uri, tls=True, tlsAllowInvalidHostnames=True, tlsAllowInvalidCertificates=True)
        else:
            self.mongodb_client = MongoClient(altas_uri)
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
    # Connection target is configurable via environment variables so CI/tests can point
    # at an ephemeral local Mongo. When these vars are unset we fall back to the existing
    # production values, so prod behavior is unchanged.
    #   MONGO_URI takes precedence over ATLAS_URI, which is kept for backward compatibility:
    #   the production .env and the data/*.py scripts still read ATLAS_URI directly.
    MONGO_URI = os.getenv('MONGO_URI') or os.getenv('ATLAS_URI')
    DB_NAME = os.getenv('MONGO_DB_NAME', 'Latin-Texts')
    DICT_DB_NAME = os.getenv('MONGO_DICT_DB_NAME', 'dictionaries')
    # Default True for Atlas; set MONGO_TLS=false for a local/CI Mongo without TLS.
    MONGO_TLS = os.getenv('MONGO_TLS', 'true').strip().lower() not in ('false', '0', 'no')

    atlas_client = AtlasClient (MONGO_URI, DB_NAME, tls=MONGO_TLS)
    atlas_client.ping()
    print('Connected to Atlas instance! We are good to go!!')
    db = atlas_client.database
    dict_db = atlas_client.get_database(DICT_DB_NAME)

except ConnectionFailure as e:
    print(f"Failed to connect to MongoDB: {e}")
    raise
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    raise




