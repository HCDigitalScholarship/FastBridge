
from fastapi import APIRouter, WebSocket, Request, File, Form, UploadFile, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import importlib
from pathlib import Path
import DefinitionTools


router = APIRouter()
router_path = Path.cwd()
templates = Jinja2Templates(directory="templates")
"""Expected Prefix: Latin/select"""

POS_list =["Noun", "Adjective", "Verb", "Preposition", "Conjunction", "Pronoun", "Number", "Adverb", "Interjection", "Proper_Noun1", "Stop_Word1"]

@router.get("/")
async def select(request : Request):
    book_name = importlib.import_module("Latin").texts
    return templates.TemplateResponse("select.html", {"request": request, "book_name": book_name})

#this is the simple result, if they exclude nothing.
@router.get("/result/{sourcetexts}/{starts}-{ends}/")
async def simple_result(request : Request, starts : str, ends : str, sourcetexts : str):
    context = {"request": request}
    triple = DefinitionTools.make_quads_or_trips(sourcetexts, starts, ends)
    words = []
    titles =[]
    for text, start, end in triple:
        book = DefinitionTools.get_text(text).book
        titles += (book.get_words(start, end))



    words = (DefinitionTools.get_definitions(titles, "Latin"))
    context["columnheaders"] = ["DISPLAY_LEMMA", "DISPLAY_LEMMA_MACRONLESS", "SIMPLE_LEMMA", "SHORT_DEFINITION", "LONG_DEFINITION", "LOCAL_DEFINITION", "PART OF SPEECH"]
    context["POS_list"] = POS_list
    #display_lemmas =([(word[0], word[3]) for word in words])
    context["words"] = words
    #print(context["words"][0])

    context["section"] =", ".join(["{text}: {start} - {end}".format(text = text.replace("_", " "), start = start, end = end) for text, start, end in triple])
    #this insane oneliner goes through the triples, and converts it to a nice, human readable, format that we render on the page.
    #context["basic_defs"] = [word[3] for word in words]
    context["len"] = len(words)
    return templates.TemplateResponse("result.html", context)

#full case, now that I worked out the simpler idea URLs wise, it is easier to keep these seperate
@router.get("/result/{sourcetexts}/{starts}-{ends}/{in_exclude}/{othertexts}/{otherstarts}-{otherends}")
async def result(request : Request, starts : str, ends : str, sourcetexts : str, in_exclude : str, othertexts : str, otherstarts : str, otherends : str):
    context = {"request": request}
    source = DefinitionTools.make_quads_or_trips(sourcetexts, starts, ends)
    other = DefinitionTools.make_quads_or_trips(othertexts, otherstarts, otherends)
    other_titles = set()
    for text, start, end in other:
        book = DefinitionTools.get_text(text).book
        other_titles = other_titles.union(set((book.get_words(start, end)))) #book.get_words gets a list of words, which we convert to a set and then union with the existing set to intersect or remove.
    other_titles = set([(new[0], new[1]) for new in other_titles]) #remove ordering information, we don't need it in this set
    ##print(other_titles)
    ##print("\n")
    titles = set()
    for text, start, end in source:
        book = DefinitionTools.get_text(text).book
        titles = titles.union(set((book.get_words(start, end))))
    to_operate = set([(new[0], new[1]) for new in titles])
    ##print(to_operate)
    ##print("\n")
    ##print(in_exclude)
    if in_exclude == "exclude":
        to_operate= to_operate.difference(other_titles)
    elif in_exclude == "include":
        to_operate.intersection_update(other_titles)

    #if always_show: #if we add lists to always include, they would be added here
        #titles = titles.union(commonly_confused) #if we make in_exclue more felxible (a list with elements in quads or trips) then we can specify for each text selected there what we do, and we can add this force show option more sensibly.
    titles =  [title for title in titles if (title[0], title[1]) in to_operate]

    ##print(titles)
    titles = sorted(titles, key=lambda x: x[-1])
    ##print(titles)
    words = (DefinitionTools.get_definitions(titles, book.language)) #this should be illegal because book should be out of scope, but it isn't.

    sextuple = list(zip(source, other))
    context["section"] =", ".join(["{text}: {start} - {end} without {other}: {other_start} - {other_end}".format(text = text[0].replace("_", " "), start = text[1], end = text[2], other = other[0].replace("_", " "), other_start= other[1], other_end = other[2]) for text, other in sextuple])
    context["columnheaders"] = ["DISPLAY_LEMMA", "DISPLAY_LEMMA_MACRONLESS", "SIMPLE_LEMMA", "SHORT_DEFINITION", "LONG_DEFINITION", "LOCAL_DEFINITION", "PART OF SPEECH"]
    context["POS_list"] = POS_list
    context["vocablist"]= words
    context["len"] = len(words)
    context["words"] = words
    return templates.TemplateResponse("result.html", context)
