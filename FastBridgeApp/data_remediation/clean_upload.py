import os
import pandas as pd
import json
import argparse
from pymongo import MongoClient
import re
from dotenv import load_dotenv

load_dotenv("FastBridgeApp/.env")

new_titles = {}
problematic_texts = []

# For general data
possible_headers = [
    "head_word", "location", "section", "orthographic_form", "case",
    "grammatical_subcategory", "lasla_subordination_code", "local_definition",
    "local_principal_parts", "counter"
]

remove_headers = ["grammatical_category", "_merge"]

target_headers = {
    "title": "head_word", 
    "headword": "head_word", 
    "text": "orthographic_form", 
    "orthographicform": "orthographic_form",
    "subordination_code": "lasla_subordination_code", 
    "laslasubordinationcode": "lasla_subordination_code",
    "partofspeech": "part_of_speech",
    "localdef": "local_definition", 
    "localdefinition": "local_definition", 
    "runningcount": "counter", 
    "grammatical_category_sub": "grammatical_subcategory",
    "grammaticalsubcategory": "grammatical_subcategory",
    "localprincipalparts": "local_principal_parts",
}

# For dictionary-specific schema
dictionary_expected_columns = [
    "TITLE", "PRINCIPAL_PARTS", "PRINCIPAL_PARTS_NO_DIACRITICALS", "SIMPLE_LEMMA",
    "SHORT_DEFINITION", "LONG_DEFINITION", "PART_OF_SPEECH", "LOGEION_LINK",
    "FORCELLINI_LINK", "ROW_FILTERS", "CONJUGATION", "DECLENSION", "PROPER",
    "REGULAR", "STOPWORD", "CORPUSFREQ", "LASLA_Combined"
]

def clean_dictionary_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [col.strip().upper().replace(" ", "_") for col in df.columns]
    missing = [col for col in dictionary_expected_columns if col not in df.columns]
    if missing:
        print(f"Missing expected columns: {missing}")
        for col in missing:
            df[col] = None
    return df[dictionary_expected_columns]

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = map(str.lower, df.columns)
    df = df.rename(columns=lambda x: "".join(x.split(" ")))
    df = df.rename(columns=target_headers)

    cleaned_df = pd.DataFrame(columns=possible_headers)
    for header in possible_headers:
        if header in df.columns:
            cleaned_df[header] = df[header]

    for header in remove_headers:
        if header in df.columns:
            df = df.drop(header, axis=1)

    for header in df.columns:
        if header not in cleaned_df.columns:
            print(f"Column '{header}' not in target schema. Skipped.")

    cleaned_df["orthographic_form"] = cleaned_df["orthographic_form"].astype(str)
    # Remove trailing .0 from location if it is a float representation
    cleaned_df["location"] = cleaned_df["location"].astype(str).str.replace(r"\.0$", "", regex=True)
    return cleaned_df

def import_dataframe_to_mongo(db: MongoClient, df: pd.DataFrame, collection_name: str, chunk_size: int = 100000):
    collection = db[collection_name]
    total_rows = len(df)
    for i in range(0, total_rows, chunk_size):
        chunk = df.iloc[i:i + chunk_size]
        records = json.loads(chunk.to_json(orient='records'))
        collection.insert_many(records)
        print(f"Inserted rows {i + 1} to {min(i + chunk_size, total_rows)} into '{collection_name}'")
        new_titles[string_to_slug(collection_name.split('_')[0])] = collection_name

def convert_and_import(folder_path: str, db: MongoClient):
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if not file_name.lower().endswith(('.xlsx', '.csv')):
                continue

            print(f"\nProcessing: {file_name}")
            file_path = os.path.join(root, file_name)
            collection_name = os.path.splitext(file_name)[0]

            if file_name.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                df = pd.read_csv(file_path)

            if database_name.lower() == 'dictionaries':
                cleaned_df = clean_dictionary_data(df)
            else:
                cleaned_df = clean_data(df)

            import_dataframe_to_mongo(db, cleaned_df, collection_name)

def string_to_slug(s: str) -> str:
    """
    
    Python version of this js code in select-stats-step-form and other js files
    
    To update this, after running code like: for collection_name in collection, initalize a dict and update it like below
    dummy_dict[string_to_slug(collection_name.split('_')[0])] = collection_name
    
    print contents of new dict and add to title_renaming_dict below
    """
    s = s.strip().lower()

    from_chars = "àáäâèéëêìíïîòóöôùúüûñç·/_,:;"
    to_chars   = "aaaaeeeeiiiioooouuuunc      "
    trans_table = str.maketrans(from_chars, to_chars)
    s = s.translate(trans_table)

    s = re.sub(r'[^a-z0-9 -]', '', s)

    s = re.sub(r'\s+', '_', s)

    return s

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", default="Texts_New_csv/Latin", help="Path to folder with Excel/CSV files")
    parser.add_argument("-c", "--collection", required=True, help="Name of the MongoDB collection")
    args = parser.parse_args()

    if not os.path.exists(args.folder):
        print(f"Folder '{args.folder}' does not exist.")
        exit(1)

    if not args.collection.endswith('-Texts') and not args.collection.endswith('-dictionaries'):
        print("Collection name must end with '-Texts' or '-dictionaries'.")
        exit(1)
        
    
    mongo_uri = os.getenv('ATLAS_URI')
    database_name = args.collection
    client = MongoClient(mongo_uri)
    db = client[database_name]

    convert_and_import(f"../data_remediation/{args.folder}", db)
    print("\nData import completed.")
    print("New titles mapping:", new_titles)
