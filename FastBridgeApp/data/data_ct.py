import os, sys
from clean_upload import string_to_slug

# Add project root to sys.path in order to import main
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import json
from collections import defaultdict
from pymongo import MongoClient

from MongoDefinitionTools import mg_get_locations

mongo_uri = os.getenv('ATLAS_URI')
print(f"Connecting to MongoDB...")

if not mongo_uri:
    print("MongoDB URI not found. Ensure you're in the right dir and .env file is set up correctly.")
    exit(1)
    
client = MongoClient(mongo_uri)

def aggregate_field_ranks(client, db_name, field_name, output_file="output_ranks.json"):
    """
    Aggregate counts of a specified field across all collections in a MongoDB database,
    and assign dense ranks based on frequency.

    Args:
        client: MongoClient instance.
        db_name (str): Name of the MongoDB database.
        field_name (str): The field name to aggregate counts for.
        output_file (str, optional): JSON file path to save the results. Defaults to "output_ranks.json".
    """
    db = client[db_name]
    counts = defaultdict(int)

    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        for doc in collection.find({}, {field_name: 1}):
            key = doc.get(field_name)
            if key:
                counts[key] += 1

    # Sort by count descending
    sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    # Assign dense ranks
    ranks = {}
    current_rank = 1
    previous_count = None
    count_at_this_rank = 0

    for key, count in sorted_items:
        if count != previous_count:
            current_rank += count_at_this_rank  # advance by how many shared last rank
            count_at_this_rank = 1
        else:
            count_at_this_rank += 1

        ranks[key] = current_rank
        previous_count = count

    # Save to file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(ranks, f, ensure_ascii=False, indent=2)

    print(f"Saved aggregated ranks to {output_file}")


def get_sections(language):
    """
    Get sections for a given language from the title renaming dictionary.
    
    Args:
        language (str): The language to get sections for.
        
    Returns:
        dict: A dictionary with section names as keys and their corresponding locations as values.
    """

    db = client[f"{language}-Texts"]
    
    # Get sections based on the title renaming dictionary
    new_sections = {}
    for text in db.list_collection_names():
        text = text.split('_')[0]
        new_sections[text] = mg_get_locations(language, string_to_slug(text))
        
    # Read current sections
    try:
        with open('FastBridgeApp/data/Static/sections.json', 'r', encoding='utf-8') as f:
            sections = json.load(f)
    except FileNotFoundError:
        sections = {}
        print("sections.json not found, creating a new one.")

    sections[language] = new_sections
    
    # Save sections to JSON
    if not os.path.exists('FastBridgeApp/data/Static'):
        os.makedirs('FastBridgeApp/data/Static')
        
    print("Saving sections to FastBridgeApp/data/Static/sections.json")
    with open('FastBridgeApp/data/Static/sections.json', 'w', encoding='utf-8') as f:
        json.dump(sections, f, ensure_ascii=False, indent=4)
    print("Sections saved to FastBridgeApp/data/Static/sections.json")

    return sections

def update_render_cache(language):
    """
    Update the render cache for titles in a given language.
    
    Args:
        language (str): The language to update the cache for.
        
    Returns:
        None
    """
    from MongoDefinitionTools import get_title_location_levels, render_titles

    cache_path = f"FastBridgeApp/data/Static/{language}_titles.json"

    print("Making new cache for", language)
    title_location_levels = get_title_location_levels(language, depth=True)
    titles = render_titles(title_location_levels)
    titles2 = render_titles(title_location_levels, dropdown="2")
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump({"titles": titles, "titles2": titles2}, f, ensure_ascii=False, indent=2)

    return titles, titles2

aggregate_field_ranks(client, "Latin-Texts", "head_word", output_file="FastBridgeApp/data/Static/latin_headword_counts.json")
aggregate_field_ranks(client, "Greek-Texts", "head_word", output_file="FastBridgeApp/data/Static/greek_headword_counts.json")

get_sections("Latin")
get_sections("Greek")

update_render_cache("Latin")
update_render_cache("Greek")