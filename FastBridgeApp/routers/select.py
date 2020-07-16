
from fastapi import APIRouter, WebSocket, Request, File, Form, UploadFile, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import importlib
from pathlib import Path
import DefinitionTools
from collections import namedtuple
from itertools import zip_longest
import math

router = APIRouter()
router_path = Path.cwd()
templates = Jinja2Templates(directory="templates")
"""Expected Prefix: /select"""


@router.get("/{language}/")
async def select(request : Request, language : str):
    book_name = importlib.import_module(language).texts #note – this imports the ENTIRE language, and takes a ton of RAM for a fraction of a second. Potentially, languages should be split up into multple files: a big one with the full lexicon (correct_dict), a huge one with the lemmata (already a seperate file) and a small one with the texts, and a small one with the filter infomration.
    return templates.TemplateResponse("select.html", {"request": request, "book_name": book_name})


def filter_helper(row_filters, POS):
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
                display_filter = f"Irregular {display_filter[:-2]}"
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
    triple = DefinitionTools.make_quads_or_trips(sourcetexts, starts, ends)
    print("made trips")
    if running_list == "running":
        running_list = True
    else:
        running_list = False
    #print(triple)
    words = []
    titles =[]
    print("entering for")
    for text, start, end in triple:
        print(text)
        book = DefinitionTools.get_text(text).book
        print("loaded the book")
        titles += (book.get_words(start, end))
    print("got titles")
    frequency_dict = {}
    if not running_list:
        dups = set()
        new_titles = []

        for title in titles:
            if (title[0]) not in dups:
                dups.add((title[0]))
                new_titles.append(title)
                frequency_dict[title[0]] = 1
            else:
                frequency_dict[title[0]] += 1


        titles = sorted(new_titles, key=lambda x: x[1])
        #print(titles)

    words, POS_list, columnheaders, row_filters, global_filters = (DefinitionTools.get_lang_data(titles, language))
    section =", ".join(["{text}: {start} - {end}".format(text = text.replace("_", " "), start = start, end = end) for text, start, end in triple])
    #this insane oneliner goes through the triples, and converts it to a nice, human readable, format that we render on the page.
    #context["basic_defs"] = [word[3] for word in words]
    if not running_list:
        columnheaders.append("Count_in_Selection")
    columnheaders.append("Order_of_Appearance")
    context["section"] = section
    context["len"] = len(words)
    length=len(columnheaders)+2 #just for some extra room
    style =f"td{{max-width: calc(100vh/{length});overflow: hidden;min-height: fit-content}}"
    context = build_html_for_clusterize(words, POS_list, columnheaders, row_filters, style, context, frequency_dict, titles, global_filters)

    print("returning")
    return templates.TemplateResponse("result.html", context)

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
    for text, start, end in other:
        book = DefinitionTools.get_text(text).book
        other_titles = other_titles.union(set((book.get_words(start, end)))) #book.get_words gets a list of words, which we convert to a set and then union with the existing set to intersect or remove.
    other_titles = set([(new[0]) for new in other_titles]) #remove ordering & local information, we don't need it in this set
    ##print("\n")
    titles = set()
    for text, start, end in source:
        book = DefinitionTools.get_text(text).book
        if not local_def:
            local_def = book.local_def
        if not local_lem:
            local_lem = book.local_lem #if any target works have them, we need it.
        titles = titles.union(set((book.get_words(start, end))))

    to_operate = set([(new[0]) for new in titles])
    ##print(to_operate)
    ##print("\n")
    ##print(in_exclude)
    sextuple = list(zip_longest(source, other, fillvalue=("","","")))
    print(sextuple)
    if in_exclude == "exclude":
        to_operate= to_operate.difference(other_titles)
        unknown = ", ".join(["{text}: {start} - {end}".format(text = text[0].replace("_", " "), start = text[1], end = text[2]) for text in source])
        known =  starts = ", ".join(["{text}: {start} - {end}".format(text = text[0].replace("_", " "), start = text[1], end = text[2]) for text in other])
        section = f"{unknown} and not in {known}"

        #", ".join(["{text}: {start} - {end} and not in {other}: {other_start} - {other_end}".format(text = text[0].replace("_", " "), start = text[1], end = text[2], other = other[0].replace("_", " "), other_start= other[1], other_end = other[2]) for text, other in sextuple])
    elif in_exclude == "include":
        to_operate= to_operate.intersection(other_titles)

        unknown = ", ".join(["{text}: {start} - {end}".format(text = text[0].replace("_", " "), start = text[1], end = text[2]) for text in source])
        known =  starts = ", ".join(["{text}: {start} - {end}".format(text = text[0].replace("_", " "), start = text[1], end = text[2]) for text in other])
        section = f"{unknown} and in {known}"
    #print(to_operate)
    #if always_show: #if we add lists to always include, they would be added here
        #titles = titles.union(commonly_confused) #if we make in_exclue more felxible (a list with elements in quads or trips) then we can specify for each text selected there what we do, and we can add this force show option more sensibly.
    frequency_dict = {}
    if not running_list:
        dups = set()

        new_titles = []
        titles  = sorted(titles, key=lambda x: x[1]) #because titles becomes a set when we in/exclude, the order we stored them in was lost
        for title in titles:
            if (title[0]) not in dups:
                dups.add((title[0]))
                new_titles.append(title)
                frequency_dict[title[0]] = 1
            else:
                frequency_dict[title[0]] += 1
        titles = new_titles
    titles =  [title for title in titles if (title[0]) in to_operate]

    ##print(titles)
    titles = sorted(titles, key=lambda x: x[1])
    ##print(titles)
    words, POS_list, columnheaders, row_filters, global_filters = (DefinitionTools.get_lang_data(titles, language, local_def, local_lem))

    if not running_list:
        columnheaders.append("Count_in_Selection")

    columnheaders.append("Order_of_Appearance")

    context["section"] = section
    context["len"] = len(words)

    length=len(columnheaders)+2 #just for some extra room
    style =f"td{{max-width: calc(100vh/{length});overflow: hidden;min-height: fit-content}}"
    context = build_html_for_clusterize(words, POS_list, columnheaders, row_filters, style, context, frequency_dict, titles, global_filters)

    #print(context["words"][0])
    return templates.TemplateResponse("result.html", context)


def build_html_for_clusterize(words, POS_list, columnheaders, row_filters, style, context, frequency_dict, titles, global_filters):
    checks = f""
    for POS in POS_list:
        filters, new_style = filter_helper(row_filters, POS)
        style+= new_style
        checks+= f'<div class="form-group"><div class="custom-control custom-checkbox"><input type="checkbox" name="filterChecks" class="custom-control-input" value="hide"  id="{POS}" onchange="hide_show_row(\'{POS}\');" checked><label class="custom-control-label" for="{POS}">{POS.replace("_", " ")}</label>'
        if filters:
            checks+= f'<span class="dropdown-submenu"> <button class="btn" onclick="document.getElementById(\'{POS}extra\').classList.toggle(\'show\')">Refine</button><ul id= "{POS}extra" class="dropdown-menu" style = "border: 0px; color:inherit;background-color:gray;"">{filters}</ul> </span>'
        checks+= f'</div></div>'
    checks+= f'<label for="global filters"> Utility Row Filters</label><div id="global filters">'
    checks+=f'<div class="form-group"><div class="custom-control custom-checkbox"><input type="checkbox" class="custom-control-input" value="hide"  id="toggle_all" onchange="toggle_all_filters(\'toggle_all\');" checked><label class="custom-control-label" for="toggle_all">Toggle All/Non</label></div></div>'
    for global_f in global_filters:
        checks+= f'<div class="form-group"><div class="custom-control custom-checkbox"><input type="checkbox" class="custom-control-input" value="hide"  id="{global_f}" onchange="global_filter(\'{global_f}\');" checked><label class="custom-control-label" for="{global_f}">{global_f.replace("_", " ").title()}</label></div></div>'
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
        if columnheaders[i] == "DISPLAY_LEMMA" or columnheaders[i] == "SHORT_DEFINITION":
            headers+= f'<input type="checkbox" class="custom-control-input" value="hide" id="{columnheaders[i]}" onchange="hide_show_column(\'{columnheaders[i]}\');" checked>'
            other_headers+=f'<th id="{columnheaders[i]}_head" class="{columnheaders[i]}" onclick="sortTable(\'{columnheaders[i]}\',{i})" >{columnheaders[i].replace("_", " ").title()}</th>'
        else:
            style+= f'.{columnheaders[i]} {{ display : none !important}}'
            header_js_obj[columnheaders[i]][0] =rules_added
            rules_added +=1
            headers+= f'<input type="checkbox" class="custom-control-input" value="show" id="{columnheaders[i]}" onchange="hide_show_column(\'{columnheaders[i]}\');">'
            other_headers+=f'<th onclick="sortTable(\'{columnheaders[i]}\',{i})" class="{columnheaders[i]}" id="{columnheaders[i]}_head">{columnheaders[i].replace("_", " ").title()}</th>'
        headers+=f'<label class="custom-control-label" for="{columnheaders[i]}">{columnheaders[i].replace("_", " ").title()}</label></div></div>'

    render_words = []

    for j in range(len(words)):
        lst = []
        to_add_to_render_words = f'<tr class="{words[j][1]}">'
        for i in range(len(columnheaders)): #removing TITLE from the column headers makes things be o
            #print(columnheaders[i][-5:])
            if columnheaders[i] == "DISPLAY_LEMMA" or columnheaders[i] == "SHORT_DEFINITION":
                to_add_to_render_words+= f'<td class="{columnheaders[i]}">{words[j][0][i+1]}</td>'
                lst.append(words[j][0][i+1])
            elif(columnheaders[i] == "LOCAL_DEFINITION"):
                to_add_to_render_words+= f'<td class="{columnheaders[i]}">{words[j][0][4]}</td>'
                lst.append(words[j][0][-4])
            elif(columnheaders[i][-5:] =="_LINK"):
                to_add_to_render_words+=f'<td class="{columnheaders[i]}"><a class="fa fa-external-link" style="font-size: 20px;" role="button" href="{words[j][0][i+1]}"> </a></td>'
                lst.append(words[j][0][i+1])
            elif(columnheaders[i] == "Count_in_Selection"):
                to_add_to_render_words+= f'<td class="{columnheaders[i]}">{frequency_dict[words[j][0][0]]}</td>'
                lst.append(frequency_dict[words[j][0][0]])
            elif(columnheaders[i] == "Order_of_Appearance"):
                to_add_to_render_words+= f'<td  class="{columnheaders[i]}">{words[j][0][-2]}</td>'
                lst.append(titles[j][1])
                #the display is the human location, but the value – which the js uses to sort – is the word number
            elif(columnheaders[i] == "Source_Text"):
                to_add_to_render_words+= f'<td class="{columnheaders[i]}">{words[j][0][-1]}</td>'
                lst.append(words[j][0][-1])
            else:
                to_add_to_render_words+= f'<td class="{columnheaders[i]}">{words[j][0][i+1]}</td>'
                lst.append(words[j][0][i+1])
        to_add_to_render_words+= f'</tr>'
        classes = words[j][1].split(' ')
        [lst.append(c) for c in classes]

        render_words.append({"values" : lst , "markup" : to_add_to_render_words, "active" : True})
    context["style"] = style
    context["headers"] = headers
    context["POS_list"] = checks
    context["filters"] = filters
    context["other_headers"]  = other_headers
    context["render_words"] = render_words
    context["columnheaders"] = header_js_obj
    return context
