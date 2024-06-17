#Meant to be a copy of DefinitionTools but with Mongo queries instead of data/*.py queries
#Currently running a local MongoDB deployment on dev droplet
import pymongo
from pymongo import MongoClient, errors
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
print('Connected to Atlas instance! We are good to go!!')

db = atlas_client.database

def main():
    #print(mg_get_slice(db, COLLECTION_NAME, 1, 117))
    #print(get_field_subset(["head_word", "corn", "counter"], COLLECTION_NAME))
    #print(mg_get_locations("Latin"))
    mg_get_location_words("Latin")


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

def get_field_subset(fields, text_name):
    '''
    Retrieve a subset of fields from all documents in a collection and return as a dictionary.
    '''
    collection = db[text_name]
    field_subset = {}

    for field in fields:
        cursor = collection.find({}, {field: 1}) 
        field_list = []
        for document in cursor:
            try:
                field_list.append(document[field])
            except KeyError:
                pass
        field_subset[field] = field_list

    return field_subset


def mg_get_slice(db, text_name, start_section, end_section):
    '''
    Retrieve documents within a specific sentence range and return a list of lists with the following format: [['head_word', 'counter', 'orthographic_form', 'local_definition', 'principal_parts', 'location', 'frequency']]
    '''
    collection = db[text_name]
    cursor = collection.find({'sentence': {'$gte': start_section, '$lte': end_section}})
    
    if cursor is None:
        return "Start or end sentence not found in the collection."
    
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
    pass
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
"""output1 = func1(*args, **kwargs)
output2 = func2(*args, **kwargs)

return output1 == output2, (output1, output2)"""


def mg_get_locations(language: str):

    """
    Get locations for all texts of a given language from MongoDB. A location is usually formatted:
    X.Y.Z where X is the book number, Y is the chapter/paragraph number, and Z is the sentence number.

    Parameters:
    language (str): The language to query for. Ie. 'Latin'

    Returns:
    text_locations: A dictionary which holds the list of locations of each text title.
        Keys: The title of the text. Eg. '50 Most Important Latin Verbs'
        Values: A dictionary which represents a linked list of locations in the text (called locations_linked_list).

            locations_linked_list: A dictionary which represent locations in a book, where each key
            points to the preceding section. 
                Keys: Represent the current section
                Values: Represent the preceding section
                    Eg. {'1.1': 'start', '1.2': '1.1', '1.3': '1.2', '1.4': '1.3', '1.5': '1.4', '1.6': '1.5'}

    Raises:
    errors.ServerSelectionTimeoutError: If the connection to the MongoDB server times out.

    """

    db = atlas_client.database

    # A dictionary to store the return value
    text_locations = {}

    # Get all collection names (text names)
    collection_names = db.list_collection_names()

    # Iterate over each collection (text) in the database
    for collection_name in collection_names:
        collection = db[collection_name]

        # Query for all documents in the collection, sorted by the 'counter' field
        documents = collection.find().sort({"counter":1})

        # locations is a list to store the location data from each document
        locations_list = ["start"]

        # Iterate over each document in the collection and extract the location data
        for doc in documents:
            location_data = doc.get("location")
            
            if isinstance(location_data, str):
                if location_data != locations_list[-1]:
                    locations_list.append((location_data))
            elif isinstance(location_data, int):
                if location_data != locations_list[-1]:
                    locations_list.append(str(location_data))
            elif isinstance(location_data, none):
                print("No location data found in document {doc['_id']}")
            else:
                print(f"Unexpected data type for 'location' in document {doc['_id']}: {type(location_data)}")
                exit(1)  

        locations_list.append("end")

        # Replaces the "_" in the location string with "."
        locations_list = format_sections(locations_list)

        # Add to locations_linked_list if locations_list is not empty
        locations_linked_list = {}
        if locations_list:
            for i in range(len(locations_list) - 1):
                locations_linked_list[locations_list[i + 1]] = locations_list[i]
            locations_linked_list["start"] = "start"
        else:
            print(f"No locations found for {collection_name}")
            exit(1)

        text_locations[collection_name] = locations_linked_list


    # print(text_locations)
    return text_locations

def mg_get_location_words(language: str):

    """
    For every text of a given language, this method gets the headword count by section 
    from MongoDB. 

    Parameters:
    language (str): The language to query for. Ie. 'Latin'

    Returns:
    all_texts_word_counts: A dictionary in which:
        Keys: The title of the text. Eg. '50 Most Important Latin Verbs'
        Values: A dictionary (called text_locations_count)... see below

            text_word_count: A dictionary in which:
                Keys: Represent a location in the text
                Values: Represent the headword count in that location
                    Eg. {'start': -1, '1': 0, '10': 1, '11': 2, ..., '9': 49, 'end': -2}

    Raises:
    errors.ServerSelectionTimeoutError: If the connection to the MongoDB server times out.

    """

    db = atlas_client.database

    # A dictionary to store the return value
    all_texts_word_counts = {}

    # Get all collection names (text names)
    collection_names = db.list_collection_names()

    # Iterate over each collection (text) in the database
    for collection_name in collection_names:
        collection = db[collection_name]

        # Query for all documents in the collection, where 'counter' field is ascending sorted
        documents = collection.find().sort({"counter":1})

        text_word_count = {"start": -1, "end": -2}

        # Iterate over each document in the collection and extract the location data
        for doc in documents:
            location_data = doc.get("location")
            
            if isinstance(location_data, str):
                if location_data not in text_word_count:
                    text_word_count[location_data.replace('_', '.')] = doc.get("counter") - 1
            elif isinstance(location_data, int):
                if location_data not in text_word_count:
                    text_word_count[location_data] = doc.get("counter") - 1
            elif isinstance(location_data, none):
                print("No location data found in document {doc['_id']}")
            else:
                print(f"Unexpected data type for 'location' in document {doc['_id']}: {type(location_data)}")
                exit(1)  

        # Check that the text has a locations word count dictionary
        if text_word_count:
            all_texts_word_counts[collection_name] = text_word_count
        else:
            print(f"No locations found for {collection_name}")
            exit(1)

    # print(all_texts_word_counts)
    return all_texts_word_counts


def format_sections(locations):
    """
    Formats a list of location strings by replacing '_' with '.'. 
    For example, '1_1_1' is converted to 1.1.1 and 58B_2 is converted to 58B.2
    
    Parameters:
    locations a list of type str: The location strings to convert.
    
    Returns: 
    locations: A list of the formatted location strings.
    
    """
    for(i, location) in enumerate(locations):
        locations[i] = locations[i].replace('_', '.') #replace underscores with periods
    
    return locations
    
    

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
