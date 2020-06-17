from fastapi import FastAPI, WebSocket, Request, File, Form, UploadFile, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import importlib
import DefinitionTools
from pathlib import Path
from pydantic import BaseModel
import add_new_text
import uvicorn
import secrets
from fastapi.responses import RedirectResponse
from typing import Optional
from routers.ToolsApp import lemmatize
from routers.sql_app import account
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
app = FastAPI()

app.include_router(lemmatize.router, prefix="/lemmatize",
    tags=["lemmatize"])
app.include_router(account.router, prefix = "/account", tags=["account"])

#going forward, the new apps should be added as routers, as explained here: https://fastapi.tiangolo.com/tutorial/bigger-applications/
#comment from 6/12/2020:
#When the redesign started, I lost track of just how many different apps there really are. It is likely that just about everything below this probably should be a router, imported the way the lemmatizer is. If you decide to change this, to minimize changes, give oracle the prefix "oracle," and copy-paste everything to do with oracle to that other file. All the user stuff probably should be a router too.  The "select" stuff is currently the default just because it is bridge's oldest functionality. It probably can be bundled up as a router too, if it is not by the time you read this.

#sql_app is not on github intentionally

#app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app_path = Path.cwd()
static_path = app_path / "static" / "assets"
app.mount("/assets", StaticFiles(directory=static_path), name="assets")

POS_list =["Noun", "Adjective", "Verb", "Particle", "Article", "Preposition", "Conjunction", "Pronoun", "Number", "Adverb", "Interjection", "Proper_Noun1", "Stop_Word1"]


@app.get("/oracle")
async def oracle_index(request : Request):
    return templates.TemplateResponse("index-oracle.html", {"request": request})

@app.get("/oracle/{language}")
async def oracle_select(request : Request, language : str):
    book_name = importlib.import_module(language).texts
    return templates.TemplateResponse("select-oracle.html", {"request": request, "book_name": book_name})

@app.get("/oracle/result/{etexts}/{e_section_size}/{known_texts}/{known_starts}-{known_ends}")
async def oracle(request : Request, etexts : str, e_section_size : str,  known_texts : str, known_starts : str, known_ends : str):
    context = {"request": request, "table_data" : []}

    table_data = []
    known = make_quads_or_trips(known_texts, known_starts, known_ends)
    ogknown_words= []
    for text, start, end in known:
        book = DefinitionTools.get_text(text).book
        ogknown_words += (book.get_words(start, end))
    ogknown_tokens = set([(new[0], new[1]) for new in ogknown_words])
    etexts =  etexts.split("+")
    e_section_size = int(e_section_size)
    for text in etexts: #actually screw it, we will just crawl the whole text. Otherwise, we need to make sections thier own data type with their own comparison operators and that is a pain. Instead, we should have them specify a section size.
        book = DefinitionTools.get_text(text).book
        sections = list(book.section_linkedlist.keys())
        for i in range(len(sections)-e_section_size):
            section = f'{sections[i]} - {sections[i+e_section_size]}'
            section_words = book.get_words(sections[i], sections[i+e_section_size])
            total_tokens = set([(new[0], new[1]) for new in section_words])
            total_words =  (section_words) #need to filter the to get out the sorting info.
            known_tokens = total_tokens.intersection(ogknown_tokens)
            count_unknown_tokens = len(total_tokens.difference(known_tokens))
            known_tokens = len(total_tokens.intersection(ogknown_tokens))

            total_tokens = len(total_tokens)
            total_words = [(new[0], new[1]) for new in total_words]
            known_words = (list_intersection(total_words, [(new[0], new[1]) for new in ogknown_words]))
            count_unknown_words = len(list_difference(total_words, known_words))

            known_words = len(known_words)
            total_words = len(total_words)

            percent1 = round(abs((known_words)/total_words) * 100, 2)
            percent_1 = f'{percent1}%'
            percent2 = round(abs((known_tokens)/total_tokens)* 100, 2)
            percent_2 = f'{percent2}%'
            link = f'/select/result/{text}/{sections[i]}-{sections[i+e_section_size]}/exclude/{known_texts}/{known_starts}-{known_ends}'
            table_data.append([section, total_words, total_tokens, known_words, known_tokens, percent_1, percent_2, link])
    context["table_data"] = sorted(table_data, key=lambda x: x[3], reverse = True)
    context["etexts"] = ", ".join([f'{text.replace("_", " ")}' for text in etexts])

    return templates.TemplateResponse("result-oracle.html", context)

def list_difference(list1, list2):
    return_list= []
    for item in list1:
        if item not in list2:
            return_list.append(item)

    return return_list

def list_intersection(list1, list2):
    """AVOID USING THIS FUNCTION IF POSSIBLE. This does set intersection on lists, but is much, much, much slower (O(smallerset) vs O(list^2))"""
    return_list = []
    for item in list1: #O(len(list1))
        if item in list2: #membership testing in lists is O(n), this is really another for loop over list2! Python sets are hash tables, so membership there is just O(1).
            return_list.append(item)

    return return_list
#End of oracle code

@app.get("/")
async def index(request : Request):
    return templates.TemplateResponse("index.html", {"request": request})
    #buttons clicked on this page will take us to /select/{language}


@app.get("/select/{language}")
async def select(request : Request, language : str):
    book_name = importlib.import_module(language).texts
    return templates.TemplateResponse("select.html", {"request": request, "book_name": book_name})



#this is the simple result, if they exclude nothing.
@app.get("/select/result/{sourcetexts}/{starts}-{ends}/")
async def simple_result(request : Request, starts : str, ends : str, sourcetexts : str):
    context = {"request": request}
    triple = make_quads_or_trips(sourcetexts, starts, ends)
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


def make_quads_or_trips(texts, starts, ends):
    texts =  texts.split("+")
    starts = starts.split("+")
    ends = ends.split("+")
    return list(zip(texts, starts, ends))


#full case, now that I worked out the simpler idea URLs wise, it is easier to keep these seperate
@app.get("/select/result/{sourcetexts}/{starts}-{ends}/{in_exclude}/{othertexts}/{otherstarts}-{otherends}")
async def result(request : Request, starts : str, ends : str, sourcetexts : str, in_exclude : str, othertexts : str, otherstarts : str, otherends : str):
    context = {"request": request}
    source = make_quads_or_trips(sourcetexts, starts, ends)
    other = make_quads_or_trips(othertexts, otherstarts, otherends)
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

 #End of select (or main?) code

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")
