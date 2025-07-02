import os, sys

# Add project root to sys.path in order to import main
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import json
from collections import defaultdict
from clean_upload import client

from text_title_rename_dict import title_renaming_dict
from MongoDefinitionTools import mg_get_locations

def aggregate_field_counts(client, db_name, field_name, output_file="output_counts.json"):
    """
    Aggregate counts of a specified field across all collections in a MongoDB database.
    Counts how many times each value appears, counting duplicates in collections.

    Args:
        client: MongoClient instance.
        db_name (str): Name of the MongoDB database.
        field_name (str): The field name to aggregate counts for.
        output_file (str, optional): JSON file path to save the results. Defaults to "output_counts.json".
    """
    db = client[db_name]
    counts = defaultdict(int)

    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        for doc in collection.find({}, {field_name: 1}):
            key = doc.get(field_name)
            if key:
                counts[key] += 1

    counts = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(counts, f, ensure_ascii=False, indent=2)

    print(f"Saved aggregated counts to {output_file}")

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
    for text in title_renaming_dict:
        new_sections[title_renaming_dict[text].split('_')[0]] = mg_get_locations(language, text)

    # Read current sections
    try:
        with open('sections.json', 'r', encoding='utf-8') as f:
            sections = json.load(f)
    except FileNotFoundError:
        sections = {}

    sections[language] = new_sections
    
    # Save sections to JSON
    with open('sections.json', 'w', encoding='utf-8') as f:
        json.dump(sections, f, ensure_ascii=False, indent=4)
    print("Sections saved to sections.json")
    
    return sections

aggregate_field_counts(client, "Latin-Texts", "head_word", output_file="FastBridgeApp/data/Static/latin_headword_counts.json")
aggregate_field_counts(client, "Greek-Texts", "head_word", output_file="FastBridgeApp/data/Static/greek_headword_counts.json")

get_sections("Latin")
get_sections("Greek")