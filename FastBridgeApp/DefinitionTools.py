import importlib
import text
from collections import namedtuple, deque
import re
#get input from the website as we have done before, that part was fine. Say they wanted sections 1.10 - 1.11 without 1.1 - 1.8.
#range_start = "1.10"
#range_end = "1.11"
#text would be a text object, but we have not built that yet

def get_text(form_request : str, language : str):
    """
    Imports the text that was requested. This way, we only load the texts that the user is requesting each time.
    """
    return importlib.import_module(f'data.{language}.{form_request}') #point to the data folder


def render_titles(language: str, dropdown : str = ""):
    book_names = importlib.import_module(f'data.{language}.texts').texts # a dict of Title: depth
    titles = []
    [titles.append(f"<a onclick=\"add_text('{key}', 'myDropdown{dropdown}', {book_names[key]})\"> {key} </a>") for key in book_names.keys()]
    return "".join(titles)

def get_sections(language: str, dropdown : str =""):
    book_names = importlib.import_module(f'data.{language}.texts').textFileDict
    sectionlist = {}
    for key in book_names:
        book = importlib.import_module(f'data.{language}.{book_names[key]}')
        sectionlist.update({book_names[key]:book.section_list})
        print(key)
    # print(sectionlist)
    return sectionlist

def get_lang_data(words : list, dictionary: str, local_defs_bool : bool = False, local_lem : bool = False):
    """
    Gets the definitions,  and other information, about the titles in words, from the appropriate dictionary, also gets the Parts of Speech (POS) and column headers to display for this language.
    This should only be called on the FINAL word list that we are returning at the end, after all the set operations have been performed.
    """
    print("gettin language data")
    lang = importlib.import_module(dictionary) #import the appropriate dictionary.
    POS =  lang.POS_list
    columnheaders = lang.columnheaders
    row_filters =  lang.row_filters
    lang = lang.correct_dict
    final_row_filters = set()
    word_list = deque() #has more effieceint appends, and is just as good to iterate over later
    #if local_defs: #we want this to be protected because it will take an extra round of iterating over all the words in the INTIAL selction.
    #local definitions are hard, because the same word could show up in the section multiple times, so we can't use a dictionary, because then we would have multiple copies of the same key.
    Word = namedtuple("Word", columnheaders + row_filters + ["Appearance", "Total_Count_in_Text", "Source_Text"])
    apperances = [word[5].replace('_', ".") for word in words]
    if local_defs_bool and local_lem:
        local_defs =[word[3] for word in words]
        local_lems =[word[4] for word in words]
        Word = namedtuple("Word", columnheaders + row_filters + ["Appearance", "Total_Count_in_Text", "Source_Text", "LOCAL_DEFINITION", "LOCAL_LEMMA"])
    elif local_defs_bool:
        local_defs =[word[3] for word in words]
        Word = namedtuple("Word", columnheaders + row_filters + ["Appearance", "Total_Count_in_Text", "Source_Text", "LOCAL_DEFINITION"])

    elif local_lem:
        local_lems =[word[4] for word in words]
        Word = namedtuple("Word", columnheaders + row_filters + ["Appearance", "Total_Count_in_Text", "Source_Text", "LOCAL_LEMMA"])
    print("defined word tuple")

    #print(words)
    nums = re.compile('[0-9]')
    computed_row_filters = deque()



    for i in range(len(words)):
        #print(words[i])
        to_add = f""
        #print(lang[words[i][0]])
        datum= (words[i][0],) + lang[words[i][0]] + (apperances[i], words[i][-2], words[i][-1])
        #print(datum)
        if local_defs_bool and local_lem:
            datum = datum + (local_defs[i], local_lems[i])
        elif local_defs_bool:
            datum = datum + (local_defs[i],)
        elif local_lem:
            datum = datum + ('', local_lems[i])



        datum = Word(*datum)
        word_list.append(datum)
        #print(datum.LOCAL_DEFINITION)
        to_add+= datum.PART_OF_SPEECH + " "
        for j in range(len(row_filters)):
            #print(row_filters[j])
            in_case_multiple = datum[len(columnheaders) + j]
            #print(in_case_multiple, "many")
            if(in_case_multiple):
                if in_case_multiple == "T":
                    in_case_multiple = "0"
                in_case_multiple = in_case_multiple.split(",")

                for case in in_case_multiple:
                    new = f"{row_filters[j]}_{datum.PART_OF_SPEECH}_{case}"
                    #print(new)
                    to_add += f"{new} "
                    final_row_filters.add((new, datum.PART_OF_SPEECH+ " "))

        computed_row_filters.append(to_add)
    del lang #this is a huge dictionary, and python's garbage collector does not delete these well. It should be destroyed when the function returns
    #print(computed_row_filters)
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
    final_row_filters.sort(key=lambda x: ((x[0][0]), int(x[0][-1])))
    #print(final_row_filters)
    POS = list(POS)
    POS.sort()
    columnheaders = columnheaders[1:] #we don't want a filter for title, that is just to make accessing dicts easier
    links = columnheaders[-2:]
    reorder = [head.lower() if head.split("_")[1]!="PARTS" else head for head in columnheaders[:-2]]


    if local_defs_bool:
        reorder.append("local_definition")
    if local_lem:
        reorder.append("local_lemma")

    reorder.sort(key=lambda x: x.split("_")[-1])
    print(reorder)
    columnheaders = [head.upper() for head in reorder]
    [columnheaders.append(link) for link in links]
    columnheaders.append("Total_Count_in_Text")

    print(columnheaders)
    filtered_global_filters = []
    for filterl in row_filters:
        if filterl=="CONJUGATION" or filterl=="DECLENSION":
            pass
        else:
            filtered_global_filters.append(f"{filterl}")

    #print(computed_row_filters)
    print(final_row_filters)
    return list(zip(word_list, computed_row_filters)), POS, columnheaders, final_row_filters, row_filters

def make_quads_or_trips(texts, starts, ends):
    """Takes the texts and starts and ends as they come in from a URL and gets them into a list of triples that are easier to deal with"""
    texts =  texts.split("+")
    starts = starts.split("+")
    ends = ends.split("+")
    return list(zip(texts, starts, ends))
