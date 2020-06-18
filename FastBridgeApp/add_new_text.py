import csv
import importlib
import os.path
from pathlib import Path
from collections import OrderedDict, namedtuple
app_path = Path.cwd()

def import_(title, section_level, csv, language):
    tempfile = csv #FastAPI recieves it as a tempfile
    filename = title.lower().replace(" ", "_").replace(",","") #get from input, what to save it as, should be the human title but lowercase and with _ instead of space, and remove commas.
    section_words = OrderedDict()
    section_words["start"] = -1
    section_words["end"] = -2
    completeName= f'{app_path}/data/{filename}.py'
    the_text = []
    section_list ={} #sections as a linked list, so that we can find the previous one really quickly
    if section_level == 1:
        section_list ={"1": "start"}
    elif section_level == 2:
        section_list ={"1.1": "start"}
    elif section_level == 3:
        section_list ={"1.1.1": "start"}

    reader = csv.readlines()
    #rows are expected to be sanitzied to come in as :TITLE	LOCATION	RUNNING COUNT	SHORTDEF  LEMMA, where SHORTDEF is the local definition and lemma is a local lemma (for dialectical differences)
    for i in range(1, len(reader)-1):
        #print(reader[i])
        row = assumed_csv_data(reader[i])
        #print(row)
        the_text.append((row[0], row[3], (int(row[2])-1)), row[4]) #add the title, definition, array index, local lemma quad to that list
        section = row[1].replace("_", ".") #change _ to . in sections, because excell messes up if this is done there
        section_words.update({section : (int(row[2])-1)} )
        #running count is number of words starting at 1, but we need them starting at 1. section_words will store the END of sections

    unique_sections = " ".join(section_words.keys()).split()
    for i in range(len(unique_sections) - 1):
        section_list[unique_sections[i+ 1]] =  unique_sections[i]
    section_list[unique_sections[-1]] = "end"
    section_list["end"] = "start"

    code = f'import text\nsection_words = {section_words}\nthe_text =  {the_text}\nsection_list ={section_list}\ntitle = "{title}"\nsection_level =  {section_level}\nlanguage = "{language}"\nbook = text.Text(title, section_words, the_text, section_list, section_level, language)'
    file1 = open(completeName, "w")
    file1.write(code)
    file1.close()

def add_words(file, language : str):
    reader = file.readlines()
    Word = namedtuple("Word", assumed_csv_data(reader[0]))
    try:
        #if the dictionary already exists
        lang = importlib.import_module(f'{language}')
        dict = lang.correct_dict

        for row in reader:
            real_row = assumed_csv_data(row)
            #the first item should be the TITLE, the rest is all the data for it.
            dict[real_row[0]] = Word(*real_row[1:])
        #now we need to save over the old file with this new dict
        code =  f'correct_dict = {dict}'
        file1 = open(f'{language}.py', "w")
        file1.write(code)
        file1.close()
        return f"updated {language}"

    except ModuleNotFoundError as e:
        #then the language does not exist in bridge yet
        dict =  {}

        headers = assumed_csv_data(reader[0])[1:]
        POS = set()
        for row in reader[1:]:
            real_row = Word(*assumed_csv_data(row))
            #the first item should be the TITLE, the rest is all the data for it.
            dict[real_row[0]] = real_row[1:]
            POS.add(real_row.Part_Of_Speech)

        columnheaders, _, row_filters = headers.partition("row_filter") #we expect the import language sheet to have this column header, but the column will be empty
        code =  f'columnheaders = {headers}\nrow_filters = {row_filters}\nPOS_list = {POS}\ncorrect_dict = {dict}'
        file1 = open(f'{language}.py', "w")
        file1.write(code)
        file1.close()
        return f"added {language}"





def assumed_csv_data(lst):
    """Takes a list of bytestrings that we are pretty sure is a csv file, but is passed on without that information. Since the user can't upload non-csvs, this is a valid assumption"""
    #print(lst)
    row = lst.decode("utf-8") #these are all bytes!
    #print(row)
    row = row.strip("\r\n") #with carriage return and new line included.
    #print(row)
    row = row.split(",")
    #print(row)
    return row
