import pandas as pd
from csv import reader
import importlib
import os.path
from pathlib import Path
from collections import OrderedDict, namedtuple
app_path = Path.cwd()
nan = ""
def import_(title, section_level, csv, language, local_def=False, local_lem=False):
    #print(csv.file)
    dataframe = pd.read_csv(csv.file, delimiter=',') #FastAPI receives it as a tempfile
    csv_reader=[list(row) for row in dataframe.values]
    filename = title.lower().replace(" ", "_").replace(",","").replace(":","").replace(")","").replace("(","").replace(".","").replace("’","").replace("&","and") #get from input, what to save it as, should be the human title but lowercase and with _ instead of space, and remove commas.
    section_words = OrderedDict()
    section_words["start"] = -1
    lang = importlib.import_module(f'{language}')
    valid =  set(lang.correct_dict.keys())
    valid.add(nan)
    del lang
    completeName= f'{app_path}/data/{language}/{filename}.py'
    the_text = []
    section_list ={} #sections as a linked list, so that we can find the previous one really quickly
    if section_level == 1:
        section_list ={"1": "start"}
    elif section_level == 2:
        section_list ={"1.1": "start"}
    elif section_level == 3:
        section_list ={"1.1.1": "start"}

    #rows are expected to be sanitzied to come in as :TITLE	LOCATION SECTION RUNNINGCOUNT TEXT (LOCAL_DEF LOCAL_LEMMA), where SHORTDEF is the local definition and lemma is a local lemma (for dialectical differences) Those last two are optional
    #we no longer use SECTION and RUNNINGCOUNT in imports
    total_frequency_dict ={}
    for i in range(len(csv_reader)):
        row =  csv_reader[i]
        try:
            total_frequency_dict[row[0]]+=1 #if it is there, increment
        except KeyError:
            total_frequency_dict[row[0]]=1


    for i in range(len(csv_reader)):
        row =  csv_reader[i]
        #print(row)
        if not (row[0] in valid): #check that the title is valid. This should be O(1)
            if pd.isna(row[0]):
                print("fine, null title")
            else:
                print("VERY BAD")
                return f'Error: {row[0]} is not defined as a word in {language}. Check line {i+2} of the import sheet if this looks like a typo, or add {row[0]} to {language}'
                #it is row i+2 because line numbers start at 1 and i starts at 0, and i does not have the headers
                assert False
        frequency = total_frequency_dict[row[0]]
        try:
            if local_def and local_lem:
                the_text.append((row[0], i, row[4], row[5], row[6], str(row[1]), frequency)) #add the title, array index,  text, definition, local lemma quad to that list
            elif local_def:
                the_text.append((row[0], i, row[4], row[5], '', str(row[1]), frequency)) #add the title, array index, text, definition
            elif local_lem:
                the_text.append((row[0], i, row[4], '', row[6], str(row[1]), frequency))
            else:
                the_text.append((row[0], i, row[4], '', '', str(row[1]), frequency))
            section = str(row[1]).replace("_", ".") #change _ to . in sections, because excell messes up if this is done there
            section_words.update({section : i} )
        except Exception as e:
            return f"Error: the row: {row} seems to be missing something. Does it have all of: TITLE, LOCATION, SECTION, RUNNINGCOUNT, TEXT and what you specified of: LOCAL_DEF, LOCAL_LEMMA"

        #running count is number of words starting at 1, but we need them starting at 1. section_words will store the END of sections
    section_words["end"] = -2
    unique_sections = " ".join(section_words.keys()).split()
    for i in range(len(unique_sections) - 1):
        section_list[unique_sections[i+ 1]] =  unique_sections[i]
    section_list["end"] = unique_sections[-2]
    section_list["start"] = "start" #unique_sections[0] = end of first section, not start of it
    section_words=dict(section_words)
    code = f'import text\nnan=""\nsection_words = {section_words}\nthe_text =  {the_text}\nsection_list ={section_list}\ntitle = "{title}"\nsection_level =  {section_level}\nlanguage = "{language}"\nbook = text.Text(title, section_words, the_text, section_list, section_level, language, {local_def}, {local_lem})'
    file1 = open(completeName, "w")
    file1.write(code)
    file1.close()

    #and add text to language/texts
    completeName = f'{app_path}/data/{language}/texts.py'
    print(completeName)
    texts = importlib.import_module(f'data.{language}.texts')
    print(texts, " current content: section level")
    print(texts.texts)
    print(texts, " current content: human to machine titles")
    print(texts.textFileDict)
    print("uploading book:", title)
    texts.texts[title] =  section_level
    texts.textFileDict[title] =  filename
    print("texts.py updated")
    print(texts.texts)
    print(texts.textFileDict)
    # https://stackoverflow.com/questions/9001509/how-can-i-sort-a-dictionary-by-key
    # sort alphabetically
    code = (
        f'texts = {dict(sorted(texts.texts.items()))} \n'
        f'textFileDict = {dict(sorted(texts.textFileDict.items()))}')
    file1 = open(completeName, "w")
    file1.write(code)
    file1.close()

    f = open("test_main.py", "a")
    #this basic test will not catch small file name errors, like trailing spaces, but will catch big ones.
    test = f"""
def test_integrity_{filename}():
    response = client.get("oracle/{language}/result/{filename}/start/end/1/{filename}/start-end")
    assert response.status_code == 200
    """
    f.write(test)
    f.close()
    return "added a text"

def add_words(file, language : str):
    dataframe = pd.read_csv(file, delimiter=',') #FastAPI receives it as a tempfile
    csv_reader=[list(row) for row in dataframe.values]
    headers = dataframe.columns.to_list()
    columnheaders, _, row_filters = " ".join(headers).partition("ROW_FILTERS") #we expect the import language sheet to have this column header, but the column will be empty


    columnheaders = columnheaders.split()
    row_filters = row_filters.split()
    print(columnheaders + row_filters)
    Word = namedtuple("Word", columnheaders+row_filters)
    try:
        #if the dictionary already exists
        lang = importlib.import_module(f'{language}')
        dict = lang.correct_dict
        POS = lang.POS_list
        assert columnheaders == lang.columnheaders
        assert row_filters == lang.row_filters


    except ModuleNotFoundError as e:
        #if the language does not exist in bridge yet
        dict =  {}
        POS = set()
        texts = set()
    except AssertionError as e:
        return f"Error: {columnheaders} is not the same as {lang.columnheaders} or {row_filters} is not the same as {lang.row_filters}"


    to_skip = headers.index("ROW_FILTERS")
    print(to_skip)
    assert to_skip != 0
    for row in csv_reader:
        #print(row)
        new = row[:to_skip]+row[to_skip+1:]
        #print(new)
        real_row = Word(*new)
        #the first item should be the TITLE, the rest is all the data for it.
        dict[real_row[0]] = real_row[1:]
        if len(real_row.PART_OF_SPEECH.split(" ")) == 1:
            POS.add(real_row.PART_OF_SPEECH)
        #else:
            #this is some thing that fits multiple exisiting POS.
    #now we need to save over the old file with this new dict
    code = f'columnheaders = {columnheaders}\nnan=""\nrow_filters = {row_filters}\nPOS_list = {POS}\ncorrect_dict = {dict}'
    file1 = open(f'{language}.py', "w")
    file1.write(code)
    file1.close()
    return f"updated {language}"

    #nan is added by pandas for empty cells in a csv file. Normally, I think it means not a number. But it is undefined in Python. We want it to be a dummy value, and since everything else is a string, the empty string makes sense. An argument could be made to define it as None, but if we more fully embrace type hints (which we should – figuring out types on the fly is slower because it is harder for the interpreter), code else where will expect a string.


def assumed_csv_data(lst):
    """Takes a list of bytestrings that we are pretty sure is a csv file, but is passed on without that information. Since the user can't upload non-csvs, this is a valid assumption"""
    print(lst)
    row = lst.decode("utf-8") #these are all bytes!
    #print(row)
    row = row.strip("\r\n") #with carriage return and new line included.
    print(row)
    row = row.split(",")
    #print(row)
    return row
