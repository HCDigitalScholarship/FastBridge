#Meant to be a copy of DefinitionTools but with Mongo queries instead of data/*.py queries
#Currently running a local MongoDB deployment on dev droplet
import pymongo
from pymongo import MongoClient, errors
import dns # required for connecting with SRV
from pymongo import MongoClient
from DefinitionTools import get_text
import text
import importlib
from collections import namedtuple, deque
import re
import time 


class AtlasClient():
    
    def __init__(self, atlas_uri, dbname):
        self.mongodb_client = MongoClient(atlas_uri, tls=True, tlsAllowInvalidHostnames=True, tlsAllowInvalidCertificates=True)
        self.database = self.mongodb_client[dbname]

    def ping(self):
        self.mongodb_client.admin.command('ping')

    def get_collection(self, collection_name):
        collection = self.database[collection_name]
        return collection

    def find(self, collection_name, filter={}, limit=0):
        collection = self.database[collection_name]
        items = list(collection.find(filter=filter, limit=limit))
        return items
    
    def get_database(self, dbname):
        selected_database = self.mongodb_client[dbname]
        return selected_database

    


# Decorators
# times the method you give to it, apply using @timer_decorator above method
def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"{func} start: ", start_time)
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func} end: ", end_time)
        elapsed_time = end_time - start_time
        print(f"{func} total time: ", elapsed_time)
        return result, elapsed_time
    return wrapper


# def connect_to_local_deployment():
# 	try:
# 		# start connection code heri

# 		uri = "mongodb://localhost:27017/"
# 		client = MongoClient(uri)

# 		# end connection code here
# 		client.admin.command("ping")
# 		print("Connected successfully")
# 		# other application code
# 		client.close()
# 	except Exception as e:
# 		raise Exception(
# 			"The following error occurred: ", e)

def get_field_subset(db, fields, text_name):
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

@timer_decorator
def mg_get_locations(db, language: str, collection_name: str):
    """
    Get all locations from a collection from MongoDB. A location is usually formatted:
    X.Y.Z where X is the book number, Y is the chapter/paragraph number, and Z is the sentence number.

    Parameters:
    db = Mongo Atlas, local deployment
    language (str): The language to query for. Ie. 'Latin' and the name of the collection.
    collection_name (str): The name of the collection to query for. Ie. '50 Most Important Latin Verbs'

    Returns:
        locations_linked_list: A dictionary which represent locations in a book, where each key
        points to the preceding section. 
            Keys: Represent the current section
            Values: Represent the preceding section
                Eg. {'1.1': 'start', '1.2': '1.1', '1.3': '1.2', '1.4': '1.3', '1.5': '1.4', '1.6': '1.5'}

    Raises:
    errors.ServerSelectionTimeoutError: If the connection to the MongoDB server times out.

    """

    collection = db[collection_name]  # Replace 'your_collection_name' with the name of your collection
    documents = collection.find().sort({"counter":1}) # Query for all documents in the collection, sorted by the 'counter' field
    locations_list = ["start"] # locations is a list to store the location data from each document

    # Iterate over each document in the collection and extract the location data
    for doc in documents:
        location_data = doc.get("location")
        if type(location_data) is str:
            if location_data != locations_list[-1]:
                locations_list.append((location_data))
        elif type(location_data) is int:
                #print(f"found int", location_data, collection_name)
            if location_data != locations_list[-1]:
                locations_list.append(str(location_data))
                #print(locations_list[-1])
        elif location_data is None:
            print(f"No location data found in document {doc['_id']}, {collection_name}")
    
    locations_list.append("end")
    locations_list = format_sections(locations_list) # Replaces the "_" in the location string with "."

    # Add to locations_linked_list if locations_list is not empty
    locations_linked_list = {}
    if locations_list:
        for i in range(len(locations_list) - 1):
            locations_linked_list[locations_list[i + 1]] = locations_list[i]
        locations_linked_list["start"] = "start"
    else:
        print(f"No locations found for {collection_name}")
        exit(1)

    #print(f"locations linked list for {collection_name}:")
    #print(locations_linked_list)
    return locations_linked_list

@timer_decorator
def mg_get_location_words(db, language: str, collection_name: str):
    """
    A text of a given language and collection name, this method gets the headword count by section 
    from MongoDB. 

    Parameters:
    db = Mongo Atlas, local deployment
    language (str): The language to query for. Ie. 'Latin'
    collection_name (str): The name of the collection to query for. Ie. '50 Most Important Latin Verbs'

    Returns:
        text_word_count: A dictionary in which:
            Keys: Represent a location in the text
            Values: Represent the headword count in that location
                Eg. {'start': -1, '1': 0, '10': 1, '11': 2, ..., '9': 49, 'end': -2}

    Raises:
    errors.ServerSelectionTimeoutError: If the connection to the MongoDB server times out.
    """

    collection = db[collection_name]

    documents = collection.find().sort({"counter":1}) # Query for all documents in the collection, where 'counter' field is ascending sorted

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
        elif isinstance(location_data, None):
            print("No location data found in document {doc['_id']}")
        else:
            print(f"Unexpected data type for 'location' in document {doc['_id']}: {type(location_data)}")
            exit(1)  

    #print(f"Text word count for {collection_name}:")
    #print(text_word_count)
    return text_word_count

def mg_render_titles(db,language: str, dropdown : str = ""):
    """
    For every text of a given language, this method writes a string of HTML code to display the text titles
    from MongoDB. 

    Parameters:
    language (str): The language to query for. Ie. 'Latin'

    Returns:
    titles: A list of HTML code to display the text titles.
    """
    title_location_levels = mg_get_location_levels(db, language) # a dict of {"Title": "location_level"}
    
    titles = []
    [titles.append(f"<a onclick=\"add_text('{key}', 'myDropdown{dropdown}', {title_location_levels[key]})\"> {key} </a>") for key in title_location_levels.keys()]
    print(titles)
    return "".join(titles)

def mg_get_location_levels(db, language: str):
    """
    For every text of a given language, this method gets the location levels
    from MongoDB. 

    Parameters:
    language (str): The language to query for. Ie. 'Latin'

    Returns:
    title_location_levels: A dictionary in which:
        Keys: The title of the text. Eg. '50 Most Important Latin Verbs'
        Values: The location levels of the text from 1 - 3. (Eg. 1 = 1, 1.1. = 2, 1.1.1 = 3)
    """
    title_location_levels = {} # A dictionary of {"Title" : location_level} to store the return value

    collection_names = db.list_collection_names() # Get all collection names (text names)

    # Iterate over each collection (text) in the database
    for collection_name in collection_names:
        collection = db[collection_name]

        location = str(collection.find_one().get("location")) # Get one document in the collection and extract the location data
        
        underscore_count = location.count("_") + 1 # Count the number of _ in the location string

        title_location_levels[collection_name] = underscore_count # Add the location level to the dictionary

    # print(title_location_levels)
    return title_location_levels


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
    

def mg_get_text(db, title: str):
    """
    function meant to retrieve the name of the collection that contains the requested text by title and language
    """
    
    
    # the list of collections to search through
    collections = db.list_collection_names()
    print(collections)

    # Iterate through collections and search for the document
    if title in collections:
        return title
    # if the document isn't found in any collection, return None
    else: 
        return None

def mg_get_lang_data(dict_db, words_from_text : list, dict_name: str, has_local_defs : bool = False, has_local_lems : bool = False):
    '''
    Gets the definitions,  and other information, about the head_words in words from the selected text, from the appropriate dictionary. 
    Also gets the Parts of Speech (POS) and column headers to display for this language.
    This should only be called on the FINAL word list that we are returning at the end, after all the set operations have been performed.
    '''

    # gather data from dictionary data in Mongo dictionary database and assign to correct variables 
    dict_data = dict_db[dict_name] 
    parts_of_speech = {'Adjective', 'Pronoun', 'Conjunction', 'Interjection', 'Noun', 'Preposition', 'Number', 'Adverb', 'Verb', 'Idiom'}
    dict_fields = ['TITLE', 'PRINCIPAL_PARTS', 'PRINCIPAL_PARTS_NO_DIACRITICALS', 'SIMPLE_LEMMA', 'SHORT_DEFINITION', 'LONG_DEFINITION', 'PART_OF_SPEECH', 'LOGEION_LINK', 'FORCELLINI_LINK']
    row_filters = ['CONJUGATION', 'DECLENSION', 'PROPER', 'REGULAR', 'STOPWORD']
    Word = namedtuple("Word", dict_fields + row_filters + ["Appearance", "Total_Count_in_Text", "Source_Text"])
    locations_list = [word[5].replace('_', ".") for word in words_from_text]
    final_row_filters = set()
    word_list = deque()
    computed_row_filters = deque()
    dict_data = build_dict_structure(dict_db, dict_name)

    # add extra fields if given text has local definitions and/or local lemmas
    if has_local_defs and has_local_lems:
        local_defs_list =[word[3] for word in words_from_text]
        local_lems_list =[word[4] for word in words_from_text]
        Word = namedtuple("Word", dict_fields + row_filters + ["Appearance", "Total_Count_in_Text", "Source_Text", "TEXT_SPECIFIC_DEFINITION", "TEXT_SPECIFIC_PRINCIPAL_PARTS"])
    elif has_local_defs:
        local_defs_list =[word[3] for word in words_from_text]
        Word = namedtuple("Word", dict_fields + row_filters + ["Appearance", "Total_Count_in_Text", "Source_Text", "TEXT_SPECIFIC_DEFINITION"])
    elif has_local_lems:
        local_lems_list =[word[4] for word in words_from_text]
        Word = namedtuple("Word", dict_fields + row_filters + ["Appearance", "Total_Count_in_Text", "Source_Text", "TEXT_SPECIFIC_PRINCIPAL_PARTS"])

    # go through every word in the given text and check for data in the row_filters fields, if more than one piece of data, split it and add both as filters in final_row_filters, if it's "T", change to "0"
    for i in range(len(words_from_text)):
        to_add = f""
        datum = (words_from_text[i][0],) + dict_data[words_from_text[i][0]] + (locations_list[i], words_from_text[i][-2], words_from_text[i][-1])
        if has_local_defs and has_local_lems:
            datum = datum + (local_defs_list[i], local_lems_list[i])
        elif has_local_defs:
            datum = datum + (local_defs_list[i],)
        elif has_local_lems:
            datum = datum + ('', local_lems_list[i])

        datum = Word(*datum)
        word_list.append(datum)
        to_add+= datum.PART_OF_SPEECH + " "

        for j in range(len(row_filters)):
            in_case_multiple = datum[len(dict_fields) + j]
            if(in_case_multiple):
                if in_case_multiple == "T":
                    in_case_multiple = "0"
                in_case_multiple = in_case_multiple.split(",")

                for case in in_case_multiple:
                    new = f"{row_filters[j]}_{datum.PART_OF_SPEECH}_{case}"
                    to_add += f"{new} "
                    final_row_filters.add((new, datum.PART_OF_SPEECH+ " "))

        computed_row_filters.append(to_add)

    del dict_data #this is a huge dictionary, and python's garbage collector does not delete these well. It should be destroyed when the function returns.

    nums = re.compile('[0-9]')
    dups = set()
    new_filters = {}
    final_row_filters = [filter for filter in final_row_filters if nums.match(filter[0][-1])]

    # clean the created filters, removing duplicate filters
    for filter in final_row_filters:
        if (filter[0]) not in dups:
            dups.add(filter[0])
            new_filters[filter[0]] = filter[1]
        else:
            new_filters[filter[0]] += filter[1]

    final_row_filters = [(k,v) for k,v in new_filters.items()]
    final_row_filters.sort(key=lambda x: ((x[0][0]), int(x[0][-1])))

    parts_of_speech = list(parts_of_speech)
    parts_of_speech.sort()

    dict_fields = dict_fields[1:] #we don't want a filter for title, that is just to make accessing dicts easier
    links = dict_fields[-2:]
    reorder = [head.lower() if head.split("_")[1]!="PARTS" else head for head in dict_fields[:-2]]

    if has_local_defs:
        reorder.append("text_specific_definition")
    if has_local_lems:
        reorder.append("TEXT_SPECIFIC_PRINCIPAL_PARTS")
    
    reorder.sort(key=lambda x: x.split("_")[-1])
    dict_fields = [head.upper() for head in reorder]
    [dict_fields.append(link) for link in links]
    dict_fields.append("Total_Count_in_Text")

    filtered_global_filters = []
    for filterl in row_filters:
        if filterl == "CONJUGATION" or filterl == "DECLENSION":
            pass
        else:
            filtered_global_filters.append(f"{filterl}")

    return list(zip(word_list, computed_row_filters)), parts_of_speech, dict_fields, final_row_filters, row_filters


def build_dict_structure(dict_db, dict_name):
    '''
    Builds a list of tuples from the MongoDB dictionary data in the same format as get_lang_data() in DefinitionTools.py does from Latin.py.
    '''
    structured_word_dict = {}
    dict_collection = dict_db[dict_name]
    exclude_fields = ["_id", "TITLE", "ROW_FILTERS", "CORPUSFREQ", "LASLA_Combined"]
    documents = dict_collection.find({})
    for doc in documents:
        head_word = doc["TITLE"]
        filtered_fields = {key: (value if value != None else '') for key, value in doc.items() if key not in exclude_fields}
        filtered_fields_tuple = tuple(filtered_fields.values())
        structured_word_dict[head_word] = filtered_fields_tuple
    return structured_word_dict

def compare_dicts(mg_built_dict):
    '''
    Compares the dictionary built using MongoDB, mg_built_dict, and the old dictionary from Latin.py by finding key discrepancies.  
    '''
    lang = importlib.import_module("Latin") #importing dictionary data from Latin.py
    lang = lang.correct_dict

    if mg_built_dict == lang:
        print("Dictionaries are the same!")
    else:
        differing_keys = set(mg_built_dict.keys()).symmetric_difference(lang.keys())

        '''for key in mg_built_dict.keys() | lang.keys():
            if mg_built_dict.get(key) != lang.get(key):
                continue
                print(f"Key '{key}':")
                print(f"  mg_built_dict value: {mg_built_dict.get(key)}")
                print(f"  lang value: {lang.get(key)}")'''

        if differing_keys:
            print("Keys in mg_built_dict or lang but not both:")
            print(f"  {differing_keys}")

#@timer_decorator
def mg_get_text_as_Text(db, language, text_title, location_list, location_words):
    '''
    Returns the specified collection as a Text object

    Parameters:
    db = Mongo Instance, local devlopment or Atlas
    language = "Latin", or "Greek"
    text_title = The title of the text as it appears in Mongo, must match the same name as a collection in DB, but will tell you if not found
    location_list = result of mg_get_locations() with the same text_title
    location_words = result of mg_get_location_words() with the same text_title

    Returns:
    A Text object(see text.py) containing all normal Text fields from that class, but adding some more fields to the_text tuples for each head_word:

    Within each Tuple:
     * = optional fields, they may not be present in every text
     ! = new field, compared to old .py file method
    [0] = head_word
    [1] = counter
    [2] = orthographic_form!
    [3] = local_definition*
    [4] = local_principal_parts*
    [5] = location 
    [6] = frequency
    [7] = sentence*
    [8] = case*! 
    [9] = lasla_subordination_code*!
    [10]= grammatical_subcategory*!


    '''    

    #Get the Text from either Atlas or Local Deployment
    print("Loading Text from MongoDB. . .")
    collection_name = mg_get_text(db, text_title)
    if(collection_name == None):
        print("Text not found")
        return
    else:
        print("Text found")
    print(f"{collection_name} successfully loaded")

    #Get all of the fields possible from the text
    all_possible_fields =  ["head_word", "location", "sentence", "counter", "orthographic_form", "case", "grammatical_subcategory", "lasla_subordination_code", "local_definition", "local_principal_parts"]
    #These are all that could appear within the headers, get_field_subset only gets the ones present in the collection
    field_data = get_field_subset(db, all_possible_fields, collection_name)#this now contains all fields present in the text file, some may not be present
    print("Fields found:")
    print(field_data.keys())
 
    #Testing field_data
    for field in field_data.keys():
        len_field = len(field_data[field])
        print(f"{field}:\t {len_field}")

    #Create boolean flags for local_def, local_lem
    local_def_flag = False
    local_lem_flag = False

    if("local_definition" in field_data.keys()):
        local_def_flag = True
    #if("local_principal_parts" in field_data.keys()):
    #local_lem_flag = True

    #Create the tuple by looping through field_data
    #the_text = (head_word, counter, orthographic_form, local definition,  local principal parts ,location, frequency count?, sentence, case, lasla_subordination_code)
    #Guaranteed Fields: ["head_word", "location", "sentence", "counter", "orthographic_form"]
    tuples = []
    frequencies = {}
    
    print("Creating tuples . . .")
   
    #Calculate word frequency within text, independent of selected range to put into tuple
    print("Calculating frequencies . . .")
    for head_word in field_data["head_word"]:
        if head_word in frequencies:
            frequencies[head_word] += 1
        else:
            frequencies[head_word] = 1

    for i in range(len(field_data["head_word"])):
        # Create a list instead of a tuple for mutability
        temp_list = [field_data["head_word"][i], field_data["counter"][i], field_data["orthographic_form"][i], "", "", field_data["location"][i], frequencies[field_data["head_word"][i]], "", "", "", ""]

        if local_def_flag:
            temp_list[3] = field_data["local_definition"][i]
        if local_lem_flag:
            temp_list[4] = field_data["local_principal_parts"][i]
        if "sentence" in field_data.keys():
            temp_list[7] = field_data["sentence"][i]
        if "case" in field_data.keys():
            temp_list[8] = field_data["case"][i]
        if "lasla_subordination_code" in field_data.keys():
            temp_list[9] = field_data["lasla_subordination_code"][i]
        if "grammatical_subcategory" in field_data.keys():
            temp_list[10] = field_data["grammatical_subcategory"][i]

        # Convert the list back to a tuple
        temp_tuple = tuple(temp_list)
        tuples.append(temp_tuple)

    #sort the tuples by counter in case it is not sorted in DB
    tuples = sorted(tuples, key=lambda word: word[1])
    print("Tuples loaded.")

    #get the section_level
    section_level = 0 #1 level for Location 1, 2 for 1_1, 3 for 1_1_1
    location_example = tuples[0][5]
    print(f"location example: {location_example}")
    if location_example == "1":
        section_level = 1
    if location_example == '1_1':
        section_level = 2
    if location_example == '1_1_1':
        section_level = 3


    #Check tuples
    for i in range(4):
        print(tuples[i])

    #check section level
    print(f"section level: {section_level}")    

    print("FInished loading text as Text!!!")
    #book = text.Text(collection_name, section_words, _____,section_list,______,"Latin",local_def_flag,local_lem_flag)
    return text.Text(collection_name, location_words, tuples, location_list, section_level, language, local_def_flag, local_lem_flag)




if __name__ == "__main__":
    main()
