from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
import MongoDefinitionTools

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def oracle_index(request: Request):
    return templates.TemplateResponse("index-oracle.html", {"request": request})


@router.get("/{language}")
async def oracle_select(request: Request, language: str):
    return templates.TemplateResponse(
        "select-oracle.html",
        {
            "request": request,
            "titles": MongoDefinitionTools.mg_render_titles(language, depth=True),
            "titles2": MongoDefinitionTools.mg_render_titles(language, dropdown="2", depth=True),
        },
    )


@router.get("/{language}/result/{etexts}/{e_section_start}/{e_section_end}/{e_units}/{e_section_size}/{known_texts}/{known_starts}-{known_ends}")
async def oracle(request: Request, language: str, etexts: str, e_units: str, e_section_size: str, known_texts: str, known_starts: str, known_ends: str, e_section_start: str, e_section_end: str):
    context = {"request": request, "table_data": []}
    table_data = []
    book_cache = {}

    def get_book(text):
        if text not in book_cache:
            book_cache[text] = MongoDefinitionTools.mg_get_text_as_Text(
                language,
                text,
                MongoDefinitionTools.mg_get_locations(language, text),
                MongoDefinitionTools.mg_get_location_words(language, text)
            )
        return book_cache[text]

    known_ranges = MongoDefinitionTools.make_quads_or_trips(known_texts, known_starts, known_ends)
    ogknown_words = []
    for text, start, end in known_ranges:
        book = get_book(text)
        ogknown_words += book.get_words(start, end)

    ogknown_wordforms = [w[0] for w in ogknown_words]
    ogknown_tokens = set(ogknown_wordforms)

    explore_ranges = MongoDefinitionTools.make_quads_or_trips(etexts, e_section_start, e_section_end)
    section_sizes = list(map(int, e_section_size.split("+")))
    sections_display = ""

    for (text, sec_start, sec_end), section_size in zip(explore_ranges, section_sizes):
        book = get_book(text)
        section_keys = list(book.section_linkedlist.keys())

        try:
            start_idx = max(0, section_keys.index(sec_end) - section_size)
        except ValueError:
            continue  # skip if section not found

        end_key = sec_end
        while start_idx >= 0 and section_keys[start_idx] != sec_start:
            start_key = section_keys[start_idx]
            section_label = f"{start_key} - {end_key}"

            section_words = book.get_words(start_key, end_key)
            wordforms = [w[0] for w in section_words]
            token_set = set(wordforms)

            known_tokens = token_set.intersection(ogknown_tokens)
            known_words = set(wordforms).intersection(ogknown_wordforms)

            total_word_count = len(wordforms)
            total_token_count = len(token_set)
            known_word_count = len(known_words)
            known_token_count = len(known_tokens)

            percent_words = f"{round(100 * known_word_count / total_word_count, 2)}%" if total_word_count else "0%"
            percent_tokens = f"{round(100 * known_token_count / total_token_count, 2)}%" if total_token_count else "0%"

            link = f"/select/{language}/result/{text}/{start_key}-{end_key}/exclude/{known_texts}/{known_starts}-{known_ends}/non_running/"

            table_data.append([section_label, total_word_count, total_token_count, known_word_count, known_token_count, percent_words, percent_tokens, link,])

            start_idx -= 1
            end_key = book.section_linkedlist.get(end_key, "start")
            if end_key == "start":
                break

        sections_display += f"{book.name}: {sec_start} - {sec_end}, "

    context["table_data"] = sorted(table_data, key=lambda row: row[3], reverse=True)
    context["etexts"] = sections_display

    return templates.TemplateResponse("result-oracle.html", context)
