
from fastapi import APIRouter, WebSocket, Request, File, Form, UploadFile, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import importlib
from pathlib import Path
import DefinitionTools

router = APIRouter()
router_path = Path.cwd()
templates = Jinja2Templates(directory="templates")
@router.get("/")
async def oracle_index(request : Request):
    return templates.TemplateResponse("index-oracle.html", {"request": request})

@router.get("/{language}")
async def oracle_select(request : Request, language : str):
    book_name = importlib.import_module(f'data.{language}.texts').texts
    return templates.TemplateResponse("select-oracle.html", {"request": request, "book_name": book_name})

@router.get("/{language}/result/{etexts}/{e_section_start}/{e_section_end}/{e_section_size}/{known_texts}/{known_starts}-{known_ends}")
async def oracle(request : Request, language : str, etexts : str, e_section_size : str,  known_texts : str, known_starts : str, known_ends : str, e_section_start : str, e_section_end : str):
    context = {"request": request, "table_data" : []}
    table_data = []
    known = DefinitionTools.make_quads_or_trips(known_texts, known_starts, known_ends)
    ogknown_words= []
    for text, start, end in known:
        book = DefinitionTools.get_text(text, language).book
        ogknown_words += (book.get_words(start, end))
    ogknown_tokens = set([(new[0]) for new in ogknown_words])
    e_section_list = e_section_size.split("+")
    to_explore = DefinitionTools.make_quads_or_trips(etexts, e_section_start, e_section_end)

    for (text, e_section_start, e_section_end), e_section_size in zip(to_explore, e_section_list):
        e_section_size = int(e_section_size)
        book = DefinitionTools.get_text(text, language).book

        #we can go through the section_linkedlist backwards
        sections = book.section_linkedlist
        indexable_sections = list(book.section_linkedlist.keys())
        print(indexable_sections)
        start = indexable_sections.index(e_section_end) - e_section_size
        end = e_section_end
        print(start)
        print(len(indexable_sections))
        while indexable_sections[start] != e_section_start:
            section = f'{indexable_sections[start]} - {end}'
            section_words = book.get_words(indexable_sections[start], end)
            total_tokens = set([(new[0]) for new in section_words])
            total_words =  (section_words) #need to filter the to get out the sorting info.
            known_tokens = total_tokens.intersection(ogknown_tokens)
            count_unknown_tokens = len(total_tokens.difference(known_tokens))
            known_tokens = len(total_tokens.intersection(ogknown_tokens))

            total_tokens = len(total_tokens)
            total_words = [(new[0], new[2]) for new in total_words]
            known_words = (list_intersection(total_words, [(new[0], new[2]) for new in ogknown_words]))
            count_unknown_words = len(list_difference(total_words, known_words))

            known_words = len(known_words)
            total_words = len(total_words)
            percent1 = round(abs((known_words)/total_words) * 100, 2)
            percent_1 = f'{percent1}%'
            percent2 = round(abs((known_tokens)/total_tokens)* 100, 2)
            percent_2 = f'{percent2}%'
            link = f'/select/{language}/result/{text}/{indexable_sections[start]}-{end}/exclude/{known_texts}/{known_starts}-{known_ends}/non_running/'
            table_data.append([section, total_words, total_tokens, known_words, known_tokens, percent_1, percent_2, link])
            start =  start - 1
            end = sections[end] #previous sections
    context["table_data"] = sorted(table_data, key=lambda x: x[3], reverse = True)
    etexts = etexts[0].replace("_" , ", ").title()
    context["etexts"] = f'{etexts} {e_section_start} - {e_section_end}'

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
