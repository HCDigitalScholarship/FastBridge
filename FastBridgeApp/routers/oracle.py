from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from MongoDefinitionTools import get_title_location_levels, render_titles, mg_get_text_as_Text, mg_get_locations, make_quads_or_trips

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def oracle_index(request: Request):
    return templates.TemplateResponse("index-oracle.html", {"request": request})


@router.get("/{language}")
async def oracle_select(request: Request, language: str):
    title_location_levels = get_title_location_levels(language, depth=True)

    return templates.TemplateResponse(
        "select-oracle.html",
        {
            "request": request,
            "titles": render_titles(title_location_levels),
            "titles2": render_titles(title_location_levels, dropdown="2"),
        },
    )


@router.get("/{language}/result/{etexts}/{e_section_start}/{e_section_end}/{e_units}/{e_section_size}/{known_texts}/{known_starts}-{known_ends}")
async def oracle(request: Request, language: str, etexts: str, e_units: str, e_section_size: str, known_texts: str, known_starts: str, known_ends: str, e_section_start: str, e_section_end: str):
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
    ogknown_words = []
    for text, start, end in known_ranges:
        ogknown_words += get_book(text).get_words(start, end,oracle=True)

    og_token_set = set(ogknown_words)

    # Prepare exploration ranges
    explore_ranges = make_quads_or_trips(etexts, e_section_start, e_section_end)
    section_sizes = list(map(int, e_section_size.split("+")))
    units = list(map(int, e_units.split("+")))
    sections_display = ""

    for (text, sec_start, sec_end), section_size, unit in zip(explore_ranges, section_sizes, units):
        book = get_book(text)
        section_keys = list(book.section_linkedlist.keys())

        try:
            start_idx = section_keys.index(sec_start) if sec_start != "start" else 0
            end_idx_limit = section_keys.index(sec_end)
            section_keys = handle_units(unit, section_keys[start_idx:end_idx_limit + 1])
            start_idx, end_idx_limit = 0, len(section_keys) - 1
        except ValueError:
            continue
        
        while start_idx + section_size - 1 <= end_idx_limit:
            end_idx = start_idx + section_size - 1
            start_key = section_keys[start_idx]
            end_key = section_keys[end_idx]
            
            # skip start and end (implicitly defined sections)
            if start_key == "start" or end_key == "end":
                start_idx += 1
                continue
            
            section_range = f"{start_key} - {end_key}"

            wordforms = book.get_words(start_key, end_key, oracle=True)
            token_set = set(wordforms)

            known_words = list_intersection(wordforms, ogknown_words)
            known_word_count = len(known_words)

            known_tokens = token_set.intersection(og_token_set)
            known_token_count = len(known_tokens)

            total_word_count = len(wordforms)
            total_token_count = len(token_set)

            percent_words = f"{round((known_word_count / total_word_count) * 100, 2)}%" if total_word_count else "0%"
            percent_tokens = f"{round((known_token_count / total_token_count) * 100, 2)}%" if total_token_count else "0%"

            link = (
                f"/select/{language}/result/{text}/{start_key}-{end_key}/exclude/"
                f"{known_texts}/{known_starts}-{known_ends}/non_running/"
            )

            table_data.append([
                section_range,
                total_word_count,
                total_token_count,
                known_word_count,
                known_token_count,
                percent_words,
                percent_tokens,
                link
            ])

            start_idx += 1  # slide window forward

        sections_display += f"{book.name}: {sec_start} - {sec_end}, "

    sections_display = sections_display.rstrip(", ")
    context["table_data"] = sorted(table_data, key=lambda row: row[3], reverse=True)
    context["etexts"] = sections_display

    return templates.TemplateResponse("result-oracle.html", context)


def list_intersection(list1, list2):
    """Returns items in both lists, preserving duplicates."""
    set2 = set(list2)
    return [item for item in list1 if item in set2]


def handle_units(unit: int, section_keys: list) -> list:
    if unit != 2 and unit != 3:
        return section_keys
    seen = set()
    filtered = []

    for key in section_keys:
        if unit == 3:
            prefix = key.split(".")[0]
        elif unit == 2:
            prefix = ".".join(key.split(".")[:2])

        if prefix not in seen:
            seen.add(prefix)
            filtered.append(key)
            
    return filtered
