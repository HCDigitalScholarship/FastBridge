import  importlib
import text
from collections import namedtuple, deque
import re
#get input from the website as we have done before, that part was fine. Say they wanted sections 1.10 - 1.11 without 1.1 - 1.8.
#range_start = "1.10"
#range_end = "1.11"
#text would be a text object, but we have not built that yet

def get_text(form_request : str):
    """
    Imports the text that was requested. This way, we only load the texts that the user is requesting each time.
    """
    return importlib.import_module(f'data.{form_request}')

def get_lang_data(words : list, dictionary: str, local_defs = False):
    """
    Gets the definitions,  and other information, about the titles in words, from the appropriate dictionary, also gets the Parts of Speech (POS) and column headers to display for this language.
    This should only be called on the FINAL word list that we are returning at the end, after all the set operations have been performed.
    """

    lang = importlib.import_module(dictionary) #import the appropriate dictionary.
    POS =  lang.POS_list
    columnheaders = lang.columnheaders[1:]
    row_filters =  lang.row_filters
    lang = lang.correct_dict
    final_row_filters = set()
    word_list = deque() #has more effieceint appends, and is just as good to iterate over later
    #if local_defs: #we want this to be protected because it will take an extra round of iterating over all the words in the INTIAL selction.
    #local definitions are hard, because the same word could show up in the section multiple times, so we can't use a dictionary, because then we would have multiple copies of the same key.
    local_defs =[word[1] for word in words]
        #in full version, text_list will be a list of tuples with the local definitions, for now it is not yet. Regardless of language, local_defs should be the second part of that tuple.
    #print(words)
    nums = re.compile('[0-9]')
    computed_row_filters = deque()
    Word = namedtuple("Word", columnheaders + row_filters + ["LOCAL_DEFINITION"])

    for i in range(len(words)):
        #print(words[i][0])
        to_add = f""
        print(lang[words[i][0]])
        datum = Word(*lang[words[i][0]], LOCAL_DEFINITION = local_defs[i])
        word_list.append(datum)
        #print(datum.LOCAL_DEFINITION)
        to_add+= datum.Part_Of_Speech + " "
        for j in range(len(row_filters)):

            in_case_multiple = datum[len(columnheaders) + j]
            if(in_case_multiple):
                in_case_multiple = in_case_multiple.split(",")
                for case in in_case_multiple:
                    new = f"{row_filters[j]}{case}"
                    to_add += f"{new} "
                    final_row_filters.add((new, datum.Part_Of_Speech+ " "))

        computed_row_filters.append(to_add)
        #if local_defs[i] != "":
            #in every language, we should have an empty final column for local definitions
            #context[words[i][0]][-1] = local_defs[i]
    dups = set()
    new_filters = {}
    final_row_filters = [filter for filter in final_row_filters if nums.match(filter[0][-1])]
    for filter in final_row_filters:
        if (filter[0]) not in dups:
            dups.add(filter[0])
            new_filters[filter[0]] = filter[1]
        else:
            new_filters[filter[0]] += filter[1]

    final_row_filters = [(k,v) for k,v in new_filters.items()]
    final_row_filters.sort(key=lambda x: ((x[0][0]), int(x[0][-1])) )
    #columnheaders.append("LOCAL_DEFINITION")
    return list(zip(word_list, computed_row_filters)), POS, columnheaders, final_row_filters

def make_quads_or_trips(texts, starts, ends):
    """Takes the texts and starts and ends as they come in from a URL and gets them into a list of triples that are easier to deal with"""
    texts =  texts.split("+")
    starts = starts.split("+")
    ends = ends.split("+")
    return list(zip(texts, starts, ends))
