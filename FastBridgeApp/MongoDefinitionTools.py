#Meant to be a copy of DefinitionTools but with Mongo queries instead of data/*.py queries
#Currently running a local MongoDB deployment on dev droplet
import pymongo
import dns # required for connecting with SRV
from pymongo import MongoClient
from DefinitionTools import get_text
from text import Text

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
COLLECTION_NAME = 'Bridge_Latin_Text_Catullus_Catullus_Catul_LASLA_LOCAL'
ATLAS_URI = "mongodb+srv://sarahruthkeim:DZBZ9E0uHh3j2FHN@test-set.zuf1otu.mongodb.net/?retryWrites=true&w=majority&appName=test-set"

atlas_client = AtlasClient (ATLAS_URI, DB_NAME)
atlas_client.ping()
print('Connected to Atlas instance! We are good to go!')

db = atlas_client.database

def main():

    print(mg_get_slice(db, COLLECTION_NAME, 1, 117))


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


#used for getting slices of each text
def mg_get_slice(db, text_name, start_section, end_section):
    collection = db[text_name]
    cursor = collection.find({'section': {'$gte': start_section, '$lte': end_section}})
    
    if cursor is None:
        return "Start or end section not found in the collection."
    
    #head_words = [document['head_word'] for document in cursor]
    
    cursor_list = list(cursor)
    document_tuple_list = list()

    for document in cursor_list:
        document_tuple = []
        for field in ['head_word', 'counter', 'orthographic_form', 'local_definition', 'principal_parts', 'location', 'frequency']:
            if field in document:
                document_tuple.append(document[field])
            else:
                document_tuple.append("")
        document_tuple_list.append(document_tuple)

    return document_tuple_list


def compare_functions(func1, func2, *args, **kwargs):
	"""
    Compares the output of two functions with the same arguments.

    Parameters:
    func1 (function): The first function to compare.
    func2 (function): The second function to compare.
    *args: Variable length argument list to pass to the functions.
    **kwargs: Arbitrary keyword arguments to pass to the functions.

    Returns:
    bool: True if the outputs are equal, False otherwise.
    tuple: The outputs of the functions.


	Example usage:
	def add(x,y):
		return x+y

	def mult(x,y):
		return x*y

	are_equal, outputs = compare_functions(add, mult, 2, 3)
    """
	output1 = func1(*args, **kwargs)
	output2 = func2(*args, **kwargs)

	return output1 == output2, (output1, output2)

def mg_get_text(title: str):
    """
    function meant to retrieve the name of the collection that contains the requested text by title and language
    """
    # Access the database
    db = atlas_client.database
    
    # the list of collections to search through
    collections = db.list_collection_names()

    # Iterate through collections and search for the document
    if title in collections:
        return title
    # if the document isn't found in any collection, return None
    else: 
        return None

if __name__ == "__main__":
    main()
