#Meant to be a copy of DefinitionTools but with Mongo queries instead of data/*.py queries
#Currently running a local MongoDB deployment on dev droplet
import pymongo
import dns # required for connecting with SRV
from pymongo import MongoClient

def connect_to_local_deployment():
	try:
		# start connection code heri

		uri = "mongodb://localhost:27017/"
		client = MongoClient(uri)

		# end connection code here
		client.admin.command("ping")
		print("Connected successfully")
		# other application code
		client.close()
	except Exception as e:
		raise Exception(
			"The following error occurred: ", e)

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

DB_NAME = 'local-dev'
COLLECTION_NAME = 'AP Latin Core List 2024_LIST'
ATLAS_URI = "mongodb+srv://sarahruthkeim:DZBZ9E0uHh3j2FHN@test-set.zuf1otu.mongodb.net/?retryWrites=true&w=majority&appName=test-set"

atlas_client = AtlasClient (ATLAS_URI, DB_NAME)
atlas_client.ping()
print('Connected to Atlas instance! We are good to go!')

section_1 = atlas_client.find(collection_name=COLLECTION_NAME, filter={"section": 1})
print(section_1)

