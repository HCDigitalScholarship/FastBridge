import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import json

load_dotenv("../../FastBridgeApp/.env")

mongo_uri = os.getenv('ATLAS_URI')
if not mongo_uri:
    print("MongoDB URI not found. Ensure you're in the right dir and .env file is set up correctly.")
    exit(1)

client = MongoClient(mongo_uri)
dict_db = client["dictionaries"]
text_dbs = {
    "Latin": client["Latin-Texts"],
    "Greek": client["Greek-Texts"]
}
dict_names = {
    "Latin": "bridge_latin_dictionary",
    "Greek": "bridge_greek_dictionary"
}

def get_excel_dups_in_folder(FOLDER_PATH, OUTPUT_FILE):
    result = {}

    for file in os.listdir(FOLDER_PATH):
        if file.endswith(".xlsx"):
            full_path = os.path.join(FOLDER_PATH, file)
            duplicates = find_duplicates_in_excel(full_path)
            if duplicates:
                result[file] = duplicates

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("{\n")
        for i, (file, rows) in enumerate(result.items()):
            f.write(f'  "{file}": [\n')
            for j, row in enumerate(rows):
                row_str = json.dumps(row, separators=(',', ': '))
                comma = ',' if j < len(rows) - 1 else ''
                f.write(f'    {row_str}{comma}\n')
            end_comma = ',' if i < len(result) - 1 else ''
            f.write(f'  ]{end_comma}\n')
        f.write("}\n")


    print(f"Duplicate report written to {OUTPUT_FILE}")


def find_duplicates_in_excel(file_path):
    try:
        df = pd.read_excel(file_path, dtype=str)
        df = df.fillna("")

        expected_cols = ["Head Word"]
        for col in expected_cols:
            if col not in df.columns:
                print(f"Missing column '{col}' in {file_path}")
                return []

        df["Original Index"] = df.index

        # Check duplicates across all four values
        subset_cols = ["Head Word"]
        duplicates = df[df.duplicated(subset=subset_cols, keep=False)]

        # Group by the subset columns to avoid listing repeated keys multiple times
        grouped = duplicates.groupby(subset_cols)
        grouped_duplicates = []

        for _, group in grouped:
            if len(group) > 1:  # Only include true duplicate groups
                output_cols = ["Original Index"] + subset_cols
                grouped_duplicates.extend(group[output_cols].values.tolist())

        return grouped_duplicates

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def get_titles_not_in_texts(language):
    """
    Find all TITLES in the dictionary that do not appear as head_word in any text.
    Save result as JSON.
    """
    dict_name = dict_names[language]
    texts_db = text_dbs[language]

    # Get all TITLES from dictionary
    dict_titles = set()
    for doc in dict_db[dict_name].find({}, {"TITLE": 1, "_id": 0}):
        if "TITLE" in doc:
            dict_titles.add(doc["TITLE"])

    # Get all head_words from all texts
    head_words = set()
    for collection_name in texts_db.list_collection_names():
        print("Checking", collection_name)
        for doc in texts_db[collection_name].find({}, {"head_word": 1, "_id": 0}):
            if "head_word" in doc:
                head_words.add(doc["head_word"])

    # Find TITLES not in head_words
    missing_titles = list(dict_titles - head_words)

    # Save to JSON
    out_path = f"missing_titles_{language}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(missing_titles, f, ensure_ascii=False, indent=2)
    print(f"Saved missing TITLES for {language} to {out_path}")

def find_texts_with_words(texts_db_name, words):
    """
    For all texts in the database, find entries where any of the input words appear as head_word.
    Returns a JSON with text collection as key and list of matching entries.
    """
    texts_db = client[texts_db_name]
    result = {}
    for collection_name in texts_db.list_collection_names():
        print("checking", collection_name)
        matches = []
        for doc in texts_db[collection_name].find({"head_word": {"$in": words}}, {"_id": 0}):
            matches.append(doc)
        if matches:
            result[collection_name] = matches

    # Save to JSON
    out_path = f"texts_with_words_{texts_db_name}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Saved texts with matching words to {out_path}")
    return result

def group_dictionary_by_lemma_and_gloss(language):
    """
    For the given language, return a dictionary with keys as (SIMPLE_LEMMA, SHORT_DEFINITION)
    and values as lists of dictionary entries that have the same SIMPLE_LEMMA and SHORT_DEFINITION.
    Saves the result to a JSON file.
    """
    dict_name = dict_names[language]
    collection = dict_db[dict_name]
    result = {}

    for doc in collection.find({}, {"_id": 0}):
        lemma = doc.get("SIMPLE_LEMMA")
        gloss = doc.get("SHORT_DEFINITION")
        if lemma and gloss:
            key = (lemma, gloss)
            key_str = f"{lemma} ; {gloss}"  
            if key_str not in result:
                result[key_str] = []
            result[key_str].append(doc)
    filtered_result = {k: v for k, v in result.items() if len(v) > 1}
    out_path = f"grouped_dictionary_{language}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(filtered_result, f, ensure_ascii=False, indent=2)
    print(f"Saved grouped dictionary for {language} to {out_path}")
    return filtered_result

def group_by_similar_definition(language, column, min_similarity_score=0.8):
    """
    Group dictionary entries that have similar SHORT_DEFINITION or LONG_DEFINITION values.
    Uses semantic similarity between definition texts (via SentenceTransformer embeddings).
    
    Args:
        language (str): The language key for dict_names and dict_db.
        column (str): "SHORT_DEFINITION" or "LONG_DEFINITION".
        min_similarity_score (float): Minimum cosine similarity for grouping.
    """
    assert column in {"SHORT_DEFINITION", "LONG_DEFINITION"}, "column must be SHORT_DEFINITION or LONG_DEFINITION"
    print(f"Getting similar definition for {language} texts based on {column}")
    
    dict_name = dict_names[language]
    collection = dict_db[dict_name]
    
    docs = list(collection.find({}, {"_id": 0, "TITLE": 1, "SIMPLE_LEMMA": 1, 
                                     "SHORT_DEFINITION": 1, "LONG_DEFINITION": 1}))
    texts = [d.get(column, "") or "" for d in docs]
    size = len(docs)
    # Load a semantic embedding model (multilingual version handles different languages)
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    embeddings = model.encode(texts, convert_to_tensor=True, show_progress_bar=True)

    result = {}

    for i, doc in enumerate(docs):
        title = doc.get("TITLE")
        if not title:
            continue
        definition_i = texts[i]
        if not definition_i.strip():
            continue

        # Compute cosine similarity to all others
        cosine_scores = util.cos_sim(embeddings[i], embeddings)[0]
        similar_docs = []
        
        for j, score in enumerate(cosine_scores):
            if i == j:
                continue
            if score >= min_similarity_score:
                d = docs[j]
                similar_docs.append({
                    "TITLE": d.get("TITLE"),
                    "SIMPLE_LEMMA": d.get("SIMPLE_LEMMA"),
                    "SHORT_DEFINITION": d.get("SHORT_DEFINITION"),
                    "LONG_DEFINITION": d.get("LONG_DEFINITION"),
                    "similarity_score": round(float(score), 3)
                })
        
        if similar_docs:
            result[title] = similar_docs
        print(f"Processed {i} of {size}")

    out_path = f"grouped_by_similarity_{language}_{column.lower()}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"Saved grouped similar definitions for {language} ({column}) to {out_path}")
    return result


if __name__ == "__main__":
    # get_excel_dups_in_folder("check/", "duplicates.json")
    # get_titles_not_in_texts("Latin")
    group_by_similar_definition("Latin", "SHORT_DEFINITION", min_similarity_score=0.95)
    # sample_words = ["AVENTINVS/N1", "AVENTINVS/N2", "AARON/N"]
    # find_texts_with_words("Latin-Texts", sample_words)
    # group_dictionary_by_lemma_and_gloss("Latin")