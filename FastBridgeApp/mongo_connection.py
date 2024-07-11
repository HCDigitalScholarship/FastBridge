from pymongo import MongoClient, errors
from pymongo.errors import ConnectionFailure


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

on_dev_server = False # change to True when working on dev server 

if on_dev_server:
    try:
        uri = 'mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.10'

        # Create a MongoClient with the URI containing authentication details
        client = MongoClient(uri)

        # Check if the connection is successful
        client.admin.command("ping")
        print("Connected successfully to MongoDB")

        db = client.get_database("Latin")
        dict_db = client.get_database("Latin-Dicts")
        print("Connected to database:", db.name)

    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
else:
    try: 
        DB_NAME = 'local-dev'
        COLLECTION_NAME = 'Bridge_Latin_Text_Catullus_Catullus_Catul_LASLA_LOCAL'
        ATLAS_URI = "mongodb+srv://sarahruthkeim:DZBZ9E0uHh3j2FHN@test-set.zuf1otu.mongodb.net/?retryWrites=true&w=majority&appName=test-set"

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
    



