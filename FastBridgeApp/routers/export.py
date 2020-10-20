from fastapi import APIRouter, WebSocket, Request, File, Form, UploadFile, Depends, HTTPException, status, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,FileResponse
import importlib
from pathlib import Path
import DefinitionTools
from collections import namedtuple
import math
import pandas as pd 
router = APIRouter()
router_path = Path.cwd()
templates = Jinja2Templates(directory="templates")
"""Expected Prefix: /export"""
import sys
import io




def filter_helper(row_filters, POS):
    print(row_filters)
    print(POS)
    loc_style = ""
    filters = f""
    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4]) #I am sorry this was too cool not to use: https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
    for filter, POS_for_filter in row_filters:
        #print(POS, POS_for_filter, "printing")
        if POS+ " " == POS_for_filter:
            display_filter = filter.replace("_", " ").title()
            if display_filter[-1] == "0":
                #print(filter, POS_for_filter, "printing")
                display_filter = display_filter[:-1]
            elif display_filter[-2:] == "99":
                display_filter = f"Irregular"
            else:
                display_filter = ordinal(int(filter[-1])) + f" {display_filter[:-1]}"
            cssclass = filter.split('_')[0]
            filters+=f'<li> <div class="custom-control custom-checkbox">   <input name="filterChecks" type="checkbox" value="hide" class="custom-control-input {cssclass}" value = "hide" id="{filter}" onchange="hide_show_row(\'{filter}\');" checked> <label class="custom-control-label" for="{filter}">{display_filter}</label></div></li>'
    return filters, loc_style

#this is the simple result, if they exclude nothing.
@router.post("/{language}/result/{sourcetexts}/{starts}-{ends}/{running_list}/")
@router.get("/{language}/result/{sourcetexts}/{starts}-{ends}/{running_list}/")
async def simple_result(request : Request, starts : str, ends : str, sourcetexts : str, language : str, running_list: str):
    context = {"request": request}

    #parse the URL, create a list of tuples with each (text, start, end)
    triple = DefinitionTools.make_quads_or_trips(sourcetexts, starts, ends)
    if running_list == "running":
        running_list = True
    else:
        running_list = False
    local_def = False
    local_lem = False
    #print(triple)
    words = []
    titles =[]
    print("entering for")
    display_triple =[]

    # iterate over each text, in triple
    for text, start, end in triple:
        print(text)
        book = DefinitionTools.get_text(text, language).book
        if not local_def:
            local_def = book.local_def
        if not local_lem:
            local_lem = book.local_lem #if any target works have them, we need it.
        display_triple.append((book.name, start, end))
        print("loaded the book")
        titles += (book.get_words(start, end))
        del book #book SHOULD be out of scope when the loop ends, but is NOT. This causes Python to hold on to the memory pool for all the lists and dictionaries in the book object. Therefore, we need to delete it ourselves
    try:
        print(book)
    except Exception as e:
        print("GOOD! IT IS GONE")
    print(local_def, local_lem)

    print("got titles")

    # what does this section do? 
    frequency_dict = {}
    if True:
        dups = set()
        new_titles = []

        for title in titles:
            if (title[0]) not in dups:
                dups.add((title[0]))
                new_titles.append(title)
                frequency_dict[title[0]] = 1
            else:
                frequency_dict[title[0]] += 1


        titles_no_dups = new_titles
        #print(titles)
        del dups
        del new_titles
    titles_no_dups = sorted(titles_no_dups, key=lambda x: x[1])
    titles = sorted(titles, key=lambda x: x[1])

    words, POS_list, columnheaders, row_filters, global_filters = (DefinitionTools.get_lang_data(titles, language, local_def, local_lem))

    words_no_dups = DefinitionTools.get_lang_data(titles_no_dups, language, local_def, local_lem)[0] #these maybe should be split up again into something like: get words from titles, get POS list for selection, get columnheaders...


    section =", ".join(["{text}: {start} - {end}".format(text = text, start = start, end = end) for text, start, end in display_triple])
    #this insane oneliner goes through the triples, and converts it to a nice, human readable, format that we render on the page.
    #context["basic_defs"] = [word[3] for word in words]
    columnheaders.append("Count_in_Selection")
    columnheaders.append("Order_of_Appearance")
    columnheaders.append("Source_Text")

    # create a list of dictionaries 
    # each dict is a word appearance and its attributes
    data = []
    df = pd.DataFrame(data)
    
    if language == 'Greek':
        for word in words:
            row = {}
            row['TITLE'] = word[0].TITLE #, ,  LOCAL_DEFINITION='report, tell'
            row['PRINCIPAL_PARTS'] = word[0].PRINCIPAL_PARTS
            row['PRINCIPAL_PARTS_NO_DIACRITICALS'] = word[0].PRINCIPAL_PARTS_NO_DIACRITICALS
            row['SIMPLE_LEMMA'] = word[0].SIMPLE_LEMMA
            row['SHORT_DEFINITION'] = word[0].SHORT_DEFINITION
            row['LONG_DEFINITION'] = word[0].LONG_DEFINITION
            row['PART_OF_SPEECH'] = word[0].PART_OF_SPEECH
            row['LOGEION_LINK'] = word[0].LOGEION_LINK
            row['CONJUNCTION'] = word[0].CONJUNCTION
            row['DECLENSION'] = word[0].DECLENSION
            row['PROPER'] = word[0].PROPER
            row['REGULAR'] = word[0].REGULAR
            row['STOPWORD'] = word[0].STOPWORD
            row['Appearance'] = word[0].Appearance
            row['Total_Count_in_Text'] = word[0].Total_Count_in_Text
            row['Source_Text'] = word[0].Source_Text
            row['LOCAL_DEFINITION'] = word[0].LOCAL_DEFINITION
            data.append(row)
            
    if language == 'Latin':
        for word in words:
            row = {}
            row["TITLE"] = word[0].TITLE
            row["PRINCIPAL_PARTS"] = word[0].PRINCIPAL_PARTS
            row["PRINCIPAL_PARTS_NO_DIACRITICALS"] = word[0].PRINCIPAL_PARTS_NO_DIACRITICALS
            row["SHORT_DEFINITION"] = word[0].SHORT_DEFINITION
            row["LONG_DEFINITION"] = word[0].LONG_DEFINITION
            row["SIMPLE_LEMMA"] = word[0].SIMPLE_LEMMA
            row["PART_OF_SPEECH"] = word[0].PART_OF_SPEECH
            row["LOGEION_LINK"] = word[0].LOGEION_LINK
            row["FORCELLINI_LINK"] = word[0].FORCELLINI_LINK
            row["Total_Count_in_Text"] = word[0].Total_Count_in_Text
            row["Source_Text"] = word[0].Source_Text
            data.append(row)

    df = pd.DataFrame(data)
    # in memory variation, not sure how to set filename
    #csv= df.to_csv()
    #return Response(content=csv, media_type="text/csv")
    csv_file_path = f'{sourcetexts}.csv'
    df.to_csv(csv_file_path, index=False)
    return FileResponse(csv_file_path, media_type="text/csv",filename=csv_file_path)

#full case, now that I worked out the simpler idea URLs wise, it is easier to keep these seperate


@router.post("/{language}/result/{sourcetexts}/{starts}-{ends}/{in_exclude}/{othertexts}/{otherstarts}-{otherends}/{running_list}/")
@router.get("/{language}/result/{sourcetexts}/{starts}-{ends}/{in_exclude}/{othertexts}/{otherstarts}-{otherends}/{running_list}/")
async def result(request : Request, starts : str, ends : str, sourcetexts : str, in_exclude : str, othertexts : str, otherstarts : str, otherends : str, language : str, running_list: str):
    context = {"request": request}
    if running_list == "running":
        running_list = True
    else:
        running_list = False
    local_def = False
    local_lem = False
    source = DefinitionTools.make_quads_or_trips(sourcetexts, starts, ends)
    other = DefinitionTools.make_quads_or_trips(othertexts, otherstarts, otherends)
    other_titles = set()
    display_triple_other =[]
    for text, start, end in other:
        book = DefinitionTools.get_text(text, language).book
        other_titles = other_titles.union(set((book.get_words(start, end)))) #book.get_words gets a list of words, which we convert to a set and then union with the existing set to intersect or remove.
        display_triple_other.append((book.name, start, end))
        del book
    other_titles = set([(new[0]) for new in other_titles]) #remove ordering & local information, we don't need it in this set
    ##print("\n")
    titles = set()
    display_triple =[]
    for text, start, end in source:
        book = DefinitionTools.get_text(text, language).book
        if not local_def:
            local_def = book.local_def
        if not local_lem:
            local_lem = book.local_lem #if any target works have them, we need it.
        display_triple.append((book.name, start, end))
        titles = titles.union(set((book.get_words(start, end))))
        del book

    to_operate = set([(new[0]) for new in titles])
    unknown = ", ".join(["{text}: {start} - {end}".format(text = text[0], start = text[1], end = text[2]) for text in display_triple])
    known =  starts = ", ".join(["{text}: {start} - {end}".format(text = text[0], start = text[1], end = text[2]) for text in display_triple_other])
    if in_exclude == "exclude":
        to_operate= to_operate.difference(other_titles)

        section = f"{unknown} and not in {known}"
    elif in_exclude == "include":
        to_operate= to_operate.intersection(other_titles)
        section = f"{unknown} and in {known}"
    frequency_dict = {}
    if True: #return no duplicates. running_list was going to toggle this, but returning all duplicates violates a data sharing agreement
        dups = set()

        new_titles = []
        for title in titles:
            if (title[0]) not in dups:
                dups.add((title[0]))
                new_titles.append(title)
                frequency_dict[title[0]] = 1
            else:
                frequency_dict[title[0]] += 1
        titles_no_dups = new_titles


    titles_no_dups = [title for title in titles_no_dups if (title[0]) in to_operate]
    titles =  [title for title in titles if (title[0]) in to_operate]



    ##print(titles)

    titles_no_dups = sorted(titles_no_dups, key=lambda x: x[1])
    titles = sorted(titles, key=lambda x: x[1])
    ##print(titles)
    words, POS_list, columnheaders, row_filters, global_filters = (DefinitionTools.get_lang_data(titles, language, local_def, local_lem))

    words_no_dups = DefinitionTools.get_lang_data(titles_no_dups, language, local_def, local_lem)[0] #these maybe should be split up again into something like: get words from titles, get POS list for selection, get columnheaders...

    columnheaders.append("Count_in_Selection")
    columnheaders.append("Order_of_Appearance")
    columnheaders.append("Source_Text")
    data = []
    
     
    if language == 'Greek':
        for word in words:
            row = {}
            row['TITLE'] = word[0].TITLE #, ,  LOCAL_DEFINITION='report, tell'
            row['PRINCIPAL_PARTS'] = word[0].PRINCIPAL_PARTS
            row['PRINCIPAL_PARTS_NO_DIACRITICALS'] = word[0].PRINCIPAL_PARTS_NO_DIACRITICALS
            row['SIMPLE_LEMMA'] = word[0].SIMPLE_LEMMA
            row['SHORT_DEFINITION'] = word[0].SHORT_DEFINITION
            row['LONG_DEFINITION'] = word[0].LONG_DEFINITION
            row['PART_OF_SPEECH'] = word[0].PART_OF_SPEECH
            row['LOGEION_LINK'] = word[0].LOGEION_LINK
            row['CONJUNCTION'] = word[0].CONJUNCTION
            row['DECLENSION'] = word[0].DECLENSION
            row['PROPER'] = word[0].PROPER
            row['REGULAR'] = word[0].REGULAR
            row['STOPWORD'] = word[0].STOPWORD
            row['Appearance'] = word[0].Appearance
            row['Total_Count_in_Text'] = word[0].Total_Count_in_Text
            row['Source_Text'] = word[0].Source_Text
            row['LOCAL_DEFINITION'] = word[0].LOCAL_DEFINITION
            data.append(row)


    if language == 'Latin':
        for word in words:
            row = {}
            row["TITLE"] = word[0].TITLE
            row["PRINCIPAL_PARTS"] = word[0].PRINCIPAL_PARTS
            row["PRINCIPAL_PARTS_NO_DIACRITICALS"] = word[0].PRINCIPAL_PARTS_NO_DIACRITICALS
            row["SHORT_DEFINITION"] = word[0].SHORT_DEFINITION
            row["LONG_DEFINITION"] = word[0].LONG_DEFINITION
            row["SIMPLE_LEMMA"] = word[0].SIMPLE_LEMMA
            row["PART_OF_SPEECH"] = word[0].PART_OF_SPEECH
            row["LOGEION_LINK"] = word[0].LOGEION_LINK
            row["FORCELLINI_LINK"] = word[0].FORCELLINI_LINK
            row["Total_Count_in_Text"] = word[0].Total_Count_in_Text
            row["Source_Text"] = word[0].Source_Text
            data.append(row)

    df = pd.DataFrame(data)
    csv_file_path = f'{sourcetexts}_{in_exclude}_{othertexts}.csv'
    df.to_csv(csv_file_path, index=False)
    return FileResponse(csv_file_path, media_type="text/csv",filename=csv_file_path)


