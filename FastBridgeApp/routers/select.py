from fastapi import APIRouter, WebSocket, Request, File, Form, UploadFile, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import importlib
import text
from pathlib import Path
import DefinitionTools
from collections import namedtuple
import math
import MongoDefinitionTools

router = APIRouter()
router_path = Path.cwd()
templates = Jinja2Templates(directory="templates")
"""Expected Prefix: /select"""
import sys


@router.get("/")
async def index(request : Request):
    print("Calling index()")
    return templates.TemplateResponse("list-index.html", {"request": request})


@router.get("/{language}/")
async def select(request : Request, language : str):
    print("Calling select()")
    return templates.TemplateResponse("select.html", {"request": request, "titles": MongoDefinitionTools.mg_render_titles(language), 'titles2': MongoDefinitionTools.mg_render_titles(language, "2") })
    # return templates.TemplateResponse("select.html", {"request": request, "titles": DefinitionTools.render_titles(language), 'titles2': DefinitionTools.render_titles(language, "2") })


@router.get("/sections/{textname}/{language}/")
async def select_section(request : Request, textname: str , language: str):
    print("Calling select_section()")
    print("Unformatted textname: ", textname)
    locations_list = MongoDefinitionTools.mg_get_locations(language, textname)
    print(f"locations_list for {textname}: ", locations_list)
    return locations_list


def filter_helper(row_filters, POS):
    print("Calling filter_helper()")
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
    print("Calling simple_result()")
    context = {"request": request}
    triple = DefinitionTools.make_quads_or_trips(sourcetexts, starts, ends)
    print("made trips")
    print("sourcetexts: ", sourcetexts)
    if running_list == "running":
        print("running list")
        running_list = True
    else:
        print("not running list")
        running_list = False
    local_def = False
    local_lem = False
    print("Printing triple: ", triple)
    words = []
    titles =[]
    print("entering for loop")
    display_triple = []
    for text, start, end in triple:
        print("Fetching locations for all texts . . . ")
        locations_list = MongoDefinitionTools.mg_get_locations(language, text)
        print("Locations loaded.")
        print("\n\nFetching all location words for all texts . . .")
        location_words = MongoDefinitionTools.mg_get_location_words(language, text)
        print("Location words loaded.\n\n")
        book = MongoDefinitionTools.mg_get_text_as_Text(language, text, locations_list, location_words)
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
    print("local_def? ", local_def, " local_lem? ", local_lem)

    print("got titles")
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
        print("titles: ", titles)
        del dups
        del new_titles
    titles_no_dups = sorted(titles_no_dups, key=lambda x: x[1])
    titles = sorted(titles, key=lambda x: x[1])

    dict_name = "bridge_latin_dictionary"
    words, POS_list, columnheaders, row_filters, global_filters = (MongoDefinitionTools.mg_get_lang_data(titles, dict_name, local_def, local_lem))
    words_no_dups = MongoDefinitionTools.mg_get_lang_data(titles_no_dups, dict_name, local_def, local_lem)[0] #these maybe should be split up again into something like: get words from titles, get POS list for selection, get columnheaders...

    section =", ".join(["{text}: {start} - {end}".format(text = text, start = start, end = end) for text, start, end in display_triple])
    #this insane oneliner goes through the triples, and converts it to a nice, human readable, format that we render on the page.
    #context["basic_defs"] = [word[3] for word in words]
    columnheaders.append("Count_in_Selection")
    columnheaders.append("Location")
    columnheaders.append("Source_Text")
    context["section"] = section
    context["len"] = len(words)
    length=len(columnheaders)+2 #just for some extra room
    style =f"td{{max-width: calc(100vh/{length});overflow: hidden;min-height: fit-content}}"
    context = build_html_for_clusterize(words, POS_list, columnheaders, row_filters, style, context, frequency_dict, titles, global_filters, words_no_dups, titles_no_dups)

    print("returning")
    response = templates.TemplateResponse("result.html", context)
    print("response made")
    return response

#full case, now that I worked out the simpler idea URLs wise, it is easier to keep these seperate


@router.post("/{language}/result/{sourcetexts}/{starts}-{ends}/{in_exclude}/{othertexts}/{otherstarts}-{otherends}/{running_list}/")
@router.get("/{language}/result/{sourcetexts}/{starts}-{ends}/{in_exclude}/{othertexts}/{otherstarts}-{otherends}/{running_list}/")
async def result(request : Request, starts : str, ends : str, sourcetexts : str, in_exclude : str, othertexts : str, otherstarts : str, otherends : str, language : str, running_list: str):
    print("Calling result()")
    context = {"request": request}
    if running_list == "running":
        running_list = True
    else:
        running_list = False
    local_def = False
    local_lem = False
    source = DefinitionTools.make_quads_or_trips(sourcetexts, starts, ends) #returns a list
    other = DefinitionTools.make_quads_or_trips(othertexts, otherstarts, otherends) #anotherList
    other_titles = set()
    display_triple_other =[]
    for text, start, end in other:
        book = MongoDefinitionTools.mg_get_text_as_Text(language, text, locations_list, location_words)
        # book = DefinitionTools.get_text(text, language).book
        other_titles = other_titles.union(set((book.get_words(start, end)))) #book.get_words gets a list of words, which we convert to a set and then union with the existing set to intersect or remove.
        display_triple_other.append((book.name, start, end))
        del book
    other_titles = set([(new[0]) for new in other_titles]) #remove ordering & local information, we don't need it in this set
    ##print("\n")
    titles = set() #builds a set
    display_triple =[]
    for text, start, end in source:
        book = DefinitionTools.get_text(text, language).book
        if not local_def:
            local_def = book.local_def
        if not local_lem:
            local_lem = book.local_lem #if any target works have them, we need it.
        display_triple.append((book.name, start, end))
        titles = titles.union(set((book.get_words(start, end)))) #get a list and then append the list to other list
        del book

    to_operate = set([(new[0]) for new in titles]) #another set
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
        titles_no_dups = new_titles #no duplicates


    titles_no_dups = [title for title in titles_no_dups if (title[0]) in to_operate]
    titles =  [title for title in titles if (title[0]) in to_operate]

    ##print(titles)

    titles_no_dups = sorted(titles_no_dups, key=lambda x: x[1])
    titles = sorted(titles, key=lambda x: x[1])
    ##print(titles)
    words, POS_list, columnheaders, row_filters, global_filters = (DefinitionTools.get_lang_data(titles, language, local_def, local_lem))

    words_no_dups = DefinitionTools.get_lang_data(titles_no_dups, language, local_def, local_lem)[0] #these maybe should be split up again into something like: get words from titles, get POS list for selection, get columnheaders...

    columnheaders.append("Count_in_Selection")
    columnheaders.append("Location")
    columnheaders.append("Source_Text")
    context["section"] = section
    context["len"] = len(words)
    length=len(columnheaders)+2 #just for some extra room
    style =f"td{{max-width: calc(100vh/{length});overflow: hidden;min-height: fit-content}}"
    context = build_html_for_clusterize(words, POS_list, columnheaders, row_filters, style, context, frequency_dict, titles, global_filters, words_no_dups, titles_no_dups)

    #print(context["words"][0])
    return templates.TemplateResponse("result.html", context)


def build_html_for_clusterize(words, POS_list, columnheaders, row_filters, style, context, frequency_dict, titles, global_filters, words_no_dups, titles_no_dups):
    print("Calling build_html_for_clusterize()")
    checks = f""
    for POS in POS_list:
        filters, new_style = filter_helper(row_filters, POS)
        style+= new_style
        checks+= f'<div class="form-group"><div class="custom-control custom-checkbox"><input type="checkbox" name="filterChecks" class="custom-control-input" value="hide"  id="{POS}" onchange="hide_show_row(\'{POS}\');" checked><label class="custom-control-label" for="{POS}">{POS.replace("_", " ")}</label>'
        if filters:
            checks+= f'<span class="dropdown-submenu"> <button class="btn btn-no-padding" onclick="document.getElementById(\'{POS}extra\').classList.toggle(\'show\')">Refine</button><ul id= "{POS}extra" class="dropdown-menu" style = "border: 0px; color:inherit;background-color:gray;"">{filters}</ul> </span>'
        checks+= f'</div></div>'
    checks+= f'<label for="global filters"> Shortcut Row Filters</label><div id="global filters">'
    for global_f in global_filters:
        display_globalf = global_f.replace("_", " ").title()
        if display_globalf == "Proper":
            display_globalf = "Proper Noun & Adjective"
        elif display_globalf == "Regular":
            display_globalf = "Regular Adjective/Adverb"
        checks+= f'<div class="form-group"><div class="custom-control custom-checkbox"><input type="checkbox" class="custom-control-input" value="hide"  id="{global_f}" onchange="global_filter(\'{global_f}\');" checked><label class="custom-control-label" for="{global_f}">{display_globalf}</label></div></div>'
    checks += '</div>'
    headers = f""
    other_headers = f""
    emtpy = [0]*len(columnheaders)
    emtpy2 = [True]*len(columnheaders)
    emtpy = [list(a) for a in zip(emtpy, emtpy2)]
    header_js_obj = dict(zip(columnheaders, emtpy)) #will be a javascript object for tracking filters
    rules_added = 1 #we set table data width in this stylesheet already
    for i in range(len(columnheaders)):
        headers+= f'<div class="form-group"> <div class="custom-control custom-checkbox">'
        if columnheaders[i] == "PRINCIPAL_PARTS" or columnheaders[i] == "SHORT_DEFINITION" or columnheaders[i] == "TEXT_SPECIFIC_DEFINITION":
            if columnheaders[i] == "SHORT_DEFINITION" and "TEXT_SPECIFIC_DEFINITION" in columnheaders:
                style+= f'.{columnheaders[i]} {{display : none !important}}'
                header_js_obj[columnheaders[i]][0] =rules_added
                rules_added +=1
                headers+= f'<input type="checkbox" class="custom-control-input" value="show" id="{columnheaders[i]}" onchange="hide_show_column(\'{columnheaders[i]}\');">'
            else:
                headers+= f'<input type="checkbox" class="custom-control-input" value="hide" id="{columnheaders[i]}" onchange="hide_show_column(\'{columnheaders[i]}\');" checked>'


        else:
            style+= f'.{columnheaders[i]} {{display : none !important}}'
            header_js_obj[columnheaders[i]][0] =rules_added
            rules_added +=1
            headers+= f'<input type="checkbox" class="custom-control-input" value="show" id="{columnheaders[i]}" onchange="hide_show_column(\'{columnheaders[i]}\');">'

        other_headers+=f'<th id="{columnheaders[i]}_head" class="{columnheaders[i]}" onclick="sortTable(\'{columnheaders[i]}\',{i})" >{columnheaders[i].replace("_", " ").title()}</th>'
        headers+=f'<label class="custom-control-label" for="{columnheaders[i]}">{columnheaders[i].replace("_", " ").title()}</label></div></div>'

    render_words = build_table(words_no_dups, columnheaders, frequency_dict, titles_no_dups)
    render_words_optional = build_table(words, columnheaders, frequency_dict, titles) #needs to be optional to comply with LALSA
    context["style"] = style
    context["headers"] = headers
    context["POS_list"] = checks
    context["filters"] = filters
    context["other_headers"]  = other_headers
    context["render_words"] = render_words
    context["render_words_optional"] = render_words_optional
    context["columnheaders"] = header_js_obj
    return context


def build_table(words: list, columnheaders: list, frequency_dict: dict, titles : dict):
    print("Calling build_table()")
    render_words = []
    print(columnheaders)
    for j in range(len(words)):
        lst = []
        #print(words[j])

        to_add_to_render_words = f'<tr class="{words[j][1]}">'
        for i in range(len(columnheaders)): #removing TITLE from the column headers makes things be o
            #print(columnheaders[i][-5:])
            if(columnheaders[i] == "LOCAL_DEFINITION"):
                to_add_to_render_words+= f'<td class="{columnheaders[i]}">{words[j][0].TEXT_SPECIFIC_DEFINITION}</td>'
                lst.append(words[j][0][-4])
            elif(columnheaders[i] == "TEXT_SPECIFIC_PRINCIPAL_PARTS"):
                to_add_to_render_words+= f'<td class="{columnheaders[i]}">{words[j][0].TEXT_SPECIFIC_PRINCIPAL_PARTS}</td>'
                lst.append(words[j][0][-3])
            elif(columnheaders[i][-5:] =="_LINK"):
                to_add_to_render_words+=f'<td class="{columnheaders[i]}"><a class="fa fa-external-link" style="font-size: 20px;" role="button" href="{words[j][0][i+1]}"> </a></td>'
                lst.append(words[j][0][i+1])
            elif(columnheaders[i] == "Count_in_Selection"):
                to_add_to_render_words+= f'<td class="{columnheaders[i]}">{frequency_dict[words[j][0][0]]}</td>'
                lst.append(frequency_dict[words[j][0][0]])
            elif(columnheaders[i] == "Location"):
                to_add_to_render_words+= f'<td class="{columnheaders[i]}">{words[j][0].Appearance}</td>'
                lst.append(titles[j][1])
                #the display is the human location, but the value – which the js uses to sort – is the word number
            elif(columnheaders[i] == "SOURCE_TEXT"):
                to_add_to_render_words+= f'<td class="{columnheaders[i]}">{words[j][0].Source_Text}</td>'
                lst.append(words[j][0][-1])
            elif(columnheaders[i] == "TOTAL_COUNT_IN_TEXT"):
                to_add_to_render_words+= f'<td class="{columnheaders[i]}">{words[j][0].Total_Count_in_Text}</td>'
                lst.append(words[j][0].Total_Count_in_Text)
            else:
                tuple_id = columnheaders[i]
                value = getattr(words[j][0], tuple_id)
                to_add_to_render_words+= f'<td class="{tuple_id}">{value}</td>'
                lst.append(value)

        to_add_to_render_words+= f'</tr>'
        classes = words[j][1].split(' ')
        [lst.append(c) for c in classes]

        render_words.append({"values" : lst , "markup" : to_add_to_render_words, "active" : True})

    return render_words
