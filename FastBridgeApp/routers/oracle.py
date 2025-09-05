from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from MongoDefinitionTools import get_title_location_levels, render_titles, mg_get_text_as_Text, mg_get_locations, make_quads_or_trips
import json

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def oracle_index(request: Request):
    return templates.TemplateResponse("index-oracle.html", {"request": request})


@router.get("/{language}")
async def oracle_select(request: Request, language: str):
    try:
        with open(f"data/Static/{language}_titles.json", "r", encoding="utf-8") as f:
            cache = json.load(f)
        titles = cache.get("titles", "")
        titles2 = cache.get("titles2", "")
    except Exception as e:
        print("Error loading titles:", e)
        title_location_levels = get_title_location_levels(language, depth=True)
        titles = render_titles(title_location_levels)
        titles2 = render_titles(title_location_levels, dropdown="2")

    return templates.TemplateResponse(
        "select-oracle.html",
        {
            "request": request,
            "titles": titles,
            "titles2": titles2,
        },
    )


@router.get("/{language}/result/{etexts}/{e_location_start}/{e_location_end}/{e_levels}/{e_location_size}/{known_texts}/{known_starts}-{known_ends}")
async def oracle(request: Request, language: str, etexts: str, e_levels: str, e_location_size: str, known_texts: str, known_starts: str, known_ends: str, e_location_start: str, e_location_end: str):
    context = {"request": request, "table_data": []}
    table_data = []
    book_cache = {}

    def get_book(text):
        location_list, location_words = mg_get_locations(language, text, get_index=True)
        if text not in book_cache:
            book_cache[text] = mg_get_text_as_Text(
                language,
                text,
                location_list,
                location_words,
            )
        return book_cache[text]

    known_ranges = make_quads_or_trips(known_texts, known_starts, known_ends)
    known_texts_display = ""
    ogknown_words = []
    for text, start, end in known_ranges:
        ogknown_words += get_book(text).get_words(start, end,oracle=True)
        known_texts_display += f"{get_book(text).name} ({start} - {end}), "

    og_token_set = set(ogknown_words)

    # Prepare exploration ranges
    explore_ranges = make_quads_or_trips(etexts, e_location_start, e_location_end)
    location_sizes = list(map(int, e_location_size.split("+")))
    levels = list(map(int, e_levels.split("+")))
    locations_display = ""

    for (text, sec_start, sec_end), location_size, level in zip(explore_ranges, location_sizes, levels):
        book = get_book(text)
        location_keys = list(book.section_linkedlist.keys())

        try:
            start_idx = location_keys.index(sec_start) if sec_start != "start" else 0
            end_idx_limit = location_keys.index(sec_end)
            location_keys = location_keys[start_idx:end_idx_limit + 1] if level == 1 else handle_levels(level, location_keys[start_idx:end_idx_limit + 1])
            start_idx, end_idx_limit = 0, len(location_keys) - 1
        except ValueError:
            continue
        
        while start_idx + location_size - 1 <= end_idx_limit:
            end_idx = start_idx + location_size - 1
            
            if level != 1:
                start_key = location_keys[start_idx][0]
                end_key = location_keys[end_idx][1]
            else:
                start_key = location_keys[start_idx]
                end_key = location_keys[end_idx]
            
            # skip start and end (implicitly defined locations)
            if start_key == "start" or end_key == "end":
                start_idx += 1
                continue
            
            location_range = f"{start_key} - {end_key}"

            wordforms = book.get_words(start_key, end_key, oracle=True)
            token_set = set(wordforms)

            known_words = list_intersection(wordforms, ogknown_words)
            known_word_count = len(known_words)

            known_tokens = token_set.intersection(og_token_set)
            known_token_count = len(known_tokens)

            total_word_count = len(wordforms)
            total_token_count = len(token_set)

            percent_words = f"{round((known_word_count / total_word_count) * 100, 1)}%" if total_word_count else "0%"
            percent_tokens = f"{round((known_token_count / total_token_count) * 100, 1)}%" if total_token_count else "0%"

            link = (
                f"/select/{language}/result/{text}/{start_key}-{end_key}/exclude/"
                f"{known_texts}/{known_starts}-{known_ends}/non_running/"
            )

            table_data.append([
                location_range,
                total_word_count,
                total_token_count,
                known_word_count,
                known_token_count,
                percent_words,
                percent_tokens,
                link
            ])

            start_idx += 1  # slide window forward

        locations_display += f"{book.name}: {sec_start} - {sec_end}, "

    locations_display = locations_display.rstrip(", ")
    context["table_data"] = sorted(table_data, key=lambda row: float(row[5].strip('%')), reverse=True) # Sort by percent_words known
    context["etexts"] = locations_display
    
    context["known_texts"] = known_texts_display.rstrip(", ")

    return templates.TemplateResponse("result-oracle.html", context)


def list_intersection(list1, list2):
    """Returns items in both lists, preserving duplicates."""
    set2 = set(list2)
    return [item for item in list1 if item in set2]


def handle_levels(level: int, location_keys: list) -> list:
    if level != 2 and level != 3: # will never be the case, but just in case
        return location_keys

    seen = {}
    for key in location_keys:
        if level == 3:
            prefix = key.split(".")[0]
        elif level == 2:
            prefix = ".".join(key.split(".")[:2])

        if prefix not in seen:
            seen[prefix] = [key, key]  # first and last key are the same for now
        else:
            seen[prefix][1] = key      # update last key

    return list(seen.values())