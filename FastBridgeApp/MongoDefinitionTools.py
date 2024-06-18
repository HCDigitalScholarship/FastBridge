#Meant to be a copy of DefinitionTools but with Mongo queries instead of data/*.py queries
#Currently running a local MongoDB deployment on dev droplet
import pymongo
from pymongo import MongoClient, errors
import dns # required for connecting with SRV
from pymongo import MongoClient
from DefinitionTools import get_text
from text import Text
import importlib
from collections import namedtuple, deque
import re

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

DB_NAME = 'local-dev'
COLLECTION_NAME = 'Bridge_Latin_Text_Catullus_Catullus_Catul_LASLA_LOCAL'
ATLAS_URI = "mongodb+srv://sarahruthkeim:DZBZ9E0uHh3j2FHN@test-set.zuf1otu.mongodb.net/?retryWrites=true&w=majority&appName=test-set"

atlas_client = AtlasClient (ATLAS_URI, DB_NAME)
atlas_client.ping()
print('Connected to Atlas instance! We are good to go!!')
db = atlas_client.database


def main():

    print(mg_get_slice(db, COLLECTION_NAME, 1, 117))

    text_name = mg_get_text("Bridge_Latin_Text_Catullus_Catullus_Catul_LASLA_LOCAL")
    print(get_field_subset(["head_word", "corn", "counter"], text_name))

    dict_db = atlas_client.get_database('dictionaries')
    words = [('ACCIPIO', 0, 'accipio', '', '', '1', 1, '50 Most Important Latin Verbs'), ('DICO/2', 1, 'dico', '', '', '10', 1, '50 Most Important Latin Verbs'), ('DO', 2, 'do', '', '', '11', 1, '50 Most Important Latin Verbs'), ('DORMIO', 3, 'dormio', '', '', '12', 1, '50 Most Important Latin Verbs'), ('DVCO', 4, 'duco', '', '', '13', 1, '50 Most Important Latin Verbs'), ('EMO', 5, 'emo', '', '', '14', 1, '50 Most Important Latin Verbs'), ('EO/1', 6, 'eo', '', '', '15', 1, '50 Most Important Latin Verbs'), ('FACIO', 7, 'facio', '', '', '16', 1, '50 Most Important Latin Verbs'), ('FERO', 8, 'fero', '', '', '17', 1, '50 Most Important Latin Verbs'), ('FVGIO', 9, 'fugio', '', '', '18', 1, '50 Most Important Latin Verbs'), ('HABEO', 10, 'habeo', '', '', '19', 1, '50 Most Important Latin Verbs'), ('AGO', 11, 'ago', '', '', '2', 1, '50 Most Important Latin Verbs'), ('INVENIO', 12, 'invenio', '', '', '20', 1, '50 Most Important Latin Verbs'), ('IVBEO', 13, 'iubeo', '', '', '21', 1, '50 Most Important Latin Verbs'), ('LEGO/2', 14, 'lego', '', '', '22', 1, '50 Most Important Latin Verbs'), ('LOQVOR', 15, 'loquor', '', '', '23', 1, '50 Most Important Latin Verbs'), ('MITTO', 16, 'mitto', '', '', '24', 1, '50 Most Important Latin Verbs'), ('MOVEO', 17, 'moveo', '', '', '25', 1, '50 Most Important Latin Verbs'), ('NOLO', 18, 'nolo', '', '', '26', 1, '50 Most Important Latin Verbs'), ('OSTENDO', 19, 'ostendo', '', '', '27', 1, '50 Most Important Latin Verbs'), ('PETO', 20, 'peto', '', '', '28', 1, '50 Most Important Latin Verbs'), ('PLACEO', 21, 'placeo', '', '', '29', 1, '50 Most Important Latin Verbs'), ('AMO', 22, 'amo', '', '', '3', 1, '50 Most Important Latin Verbs'), ('PONO', 23, 'pono', '', '', '30', 1, '50 Most Important Latin Verbs'), ('POSSVM/1', 24, 'possum', '', '', '31', 1, '50 Most Important Latin Verbs'), ('PVTO', 25, 'puto', '', '', '32', 1, '50 Most Important Latin Verbs'), ('QVAERO', 26, 'quaero', '', '', '33', 1, '50 Most Important Latin Verbs'), ('RELINQVO', 27, 'relinquo', '', '', '34', 1, '50 Most Important Latin Verbs'), ('SCIO', 28, 'scio', '', '', '35', 1, '50 Most Important Latin Verbs'), ('SCRIBO', 29, 'scribo', '', '', '36', 1, '50 Most Important Latin Verbs'), ('SEDEO', 30, 'sedeo', '', '', '37', 1, '50 Most Important Latin Verbs'), ('SOLEO', 31, 'soleo', '', '', '38', 1, '50 Most Important Latin Verbs'), ('STO', 32, 'sto', '', '', '39', 1, '50 Most Important Latin Verbs'), ('AVDIO', 33, 'audio', '', '', '4', 1, '50 Most Important Latin Verbs'), ('SVM/1', 34, 'sum', '', '', '40', 1, '50 Most Important Latin Verbs'), ('SVMO', 35, 'sumo', '', '', '41', 1, '50 Most Important Latin Verbs'), ('SVRGO', 36, 'surgo', '', '', '42', 1, '50 Most Important Latin Verbs'), ('TENEO', 37, 'teneo', '', '', '43', 1, '50 Most Important Latin Verbs'), ('TIMEO', 38, 'timeo', '', '', '44', 1, '50 Most Important Latin Verbs'), ('VENIO', 39, 'venio', '', '', '45', 1, '50 Most Important Latin Verbs'), ('VERTO', 40, 'verto', '', '', '46', 1, '50 Most Important Latin Verbs'), ('VIDEO', 41, 'video', '', '', '47', 1, '50 Most Important Latin Verbs'), ('VOCO', 42, 'voco', '', '', '48', 1, '50 Most Important Latin Verbs'), ('VOLO/3', 43, 'volo', '', '', '49', 1, '50 Most Important Latin Verbs'), ('CAPIO/2', 44, 'capio', '', '', '5', 1, '50 Most Important Latin Verbs'), ('VTOR', 45, 'utor', '', '', '50', 1, '50 Most Important Latin Verbs'), ('COMEDO/2', 46, 'comedo', '', '', '6', 1, '50 Most Important Latin Verbs'), ('CONOR', 47, 'conor', '', '', '7', 1, '50 Most Important Latin Verbs'), ('CREDO', 48, 'credo', '', '', '8', 1, '50 Most Important Latin Verbs'), ('DEBEO', 49, 'debeo', '', '', '9', 1, '50 Most Important Latin Verbs')] 
    print(mg_get_lang_data(dict_db, words, "bridge_latin_dictionary"))
    #def_tools_result = ([(Word(TITLE='POST/2', PRINCIPAL_PARTS='post', PRINCIPAL_PARTS_NO_DIACRITICALS='post', SIMPLE_LEMMA='post', SHORT_DEFINITION='after (adv. and prep. +acc.)', LONG_DEFINITION='after(ward), later; behind (+ acc.)', PART_OF_SPEECH='Preposition', LOGEION_LINK='http://logeion.uchicago.edu/index.html#post', FORCELLINI_LINK='http://lexica.linguax.com/forc2.php?searchedLG=post', CONJUGATION='', DECLENSION='', PROPER='', REGULAR='', STOPWORD='T', Appearance='5', Total_Count_in_Text=3, Source_Text='Abelard, Historia Calamitatum 5-6'), 'Preposition STOPWORD_Preposition_0 '), (Word(TITLE='PAVCI', PRINCIPAL_PARTS='paucus –a –um', PRINCIPAL_PARTS_NO_DIACRITICALS='paucus –a –um', SIMPLE_LEMMA='paucus', SHORT_DEFINITION='(pl.) a few; (sing.) small', LONG_DEFINITION='(pl.) a few; (sing.) small', PART_OF_SPEECH='Adjective', LOGEION_LINK='http://logeion.uchicago.edu/index.html#paucus', FORCELLINI_LINK='http://lexica.linguax.com/forc2.php?searchedLG=paucus', CONJUGATION='', DECLENSION='1', PROPER='', REGULAR='', STOPWORD='', Appearance='5', Total_Count_in_Text=2, Source_Text='Abelard, Historia Calamitatum 5-6'), 'Adjective DECLENSION_Adjective_1 '), (Word(TITLE='ITAQVE', PRINCIPAL_PARTS='itaque', PRINCIPAL_PARTS_NO_DIACRITICALS='itaque', SIMPLE_LEMMA='itaque', SHORT_DEFINITION='and so therefore', LONG_DEFINITION='and so, accordingly; thus, therefore, consequently', PART_OF_SPEECH='Adverb', LOGEION_LINK='http://logeion.uchicago.edu/index.html#itaque', FORCELLINI_LINK='http://lexica.linguax.com/forc2.php?searchedLG=itaque', CONJUGATION='', DECLENSION='', PROPER='', REGULAR='', STOPWORD='', Appearance='5', Total_Count_in_Text=7, Source_Text='Abelard, Historia Calamitatum 5-6'), 'Adverb '), (Word(TITLE='DIES', PRINCIPAL_PARTS='diēs diēī m. or f.', PRINCIPAL_PARTS_NO_DIACRITICALS='dies diei m. or f.', SIMPLE_LEMMA='dies', SHORT_DEFINITION='day', LONG_DEFINITION='day', PART_OF_SPEECH='Noun', LOGEION_LINK='http://logeion.uchicago.edu/index.html#dies', FORCELLINI_LINK='http://lexica.linguax.com/forc2.php?searchedLG=dies', CONJUGATION='', DECLENSION='5', PROPER='', REGULAR='', STOPWORD='', Appearance='5', Total_Count_in_Text=2, Source_Text='Abelard, Historia Calamitatum 5-6'), 'Noun DECLENSION_Noun_5 '), (Word(TITLE='PARISIVS/A', PRINCIPAL_PARTS='Parīsius –a –um', PRINCIPAL_PARTS_NO_DIACRITICALS='Parisius –a –um', SIMPLE_LEMMA='Parisius', SHORT_DEFINITION='of or from Paris (place)', LONG_DEFINITION='of or from Paris (city); subst. esp., the Celtic tribe from this region', PART_OF_SPEECH='Adjective', LOGEION_LINK='http://logeion.uchicago.edu/index.html#Parisius', FORCELLINI_LINK='http://lexica.linguax.com/forc2.php?searchedLG=Parisius', CONJUGATION='', DECLENSION='1', PROPER='T', REGULAR='', STOPWORD='', Appearance='5', Total_Count_in_Text=2, Source_Text='Abelard, Historia Calamitatum 5-6'), 'Adjective DECLENSION_Adjective_1 PROPER_Adjective_0 ')], ['Adjective', 'Adverb', 'Conjunction', 'Idiom', 'Interjection', 'Noun', 'Number', 'Preposition', 'Pronoun', 'Verb'], ['PRINCIPAL_PARTS_NO_DIACRITICALS', 'PRINCIPAL_PARTS', 'SHORT_DEFINITION', 'LONG_DEFINITION', 'SIMPLE_LEMMA', 'PART_OF_SPEECH', 'LOGEION_LINK', 'FORCELLINI_LINK', 'Total_Count_in_Text'], [('DECLENSION_Adjective_1', 'Adjective '), ('DECLENSION_Noun_5', 'Noun '), ('PROPER_Adjective_0', 'Adjective '), ('STOPWORD_Preposition_0', 'Preposition ')], ['CONJUGATION', 'DECLENSION', 'PROPER', 'REGULAR', 'STOPWORD'])
    #print(compare_results(mongo_def_tools_result, def_tools_result))


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
    text_locations: A dictionary which holds the list of locations of each text text title.
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
        else:
            print(f"No locations found for {collection_name}")
            exit(1)

        text_locations[collection_name] = locations_linked_list

    #print(text_locations)
    return text_locations


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


if __name__ == "__main__":
    main()
