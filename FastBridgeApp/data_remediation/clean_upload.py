import os
import pandas as pd
import json
import argparse
from pymongo import MongoClient
import re
from dotenv import load_dotenv

load_dotenv("../../FastBridgeApp/.env")

new_titles = {}
problematic_texts = {}
dict_db = None
checked_words = set()

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
    "laslasubordinationcode": "lasla_subordination_code",
    "partofspeech": "part_of_speech",
    "localdef": "local_definition", 
    "localdefinition": "local_definition", 
    "runningcount": "counter", 
    "grammatical_category_sub": "grammatical_subcategory",
    "grammaticalsubcategory": "grammatical_subcategory",
    "localprincipalparts": "local_principal_parts",
}

text_cols_to_check = [
    "head_word", "location", "section", "orthographic_form", "counter"
]

dict_cols_to_check = [
    "TITLE", "PRINCIPAL_PARTS", "PRINCIPAL_PARTS_NO_DIACRITICALS", "SHORT_DEFINITION",
]

# For dictionary-specific schema
dictionary_expected_columns = [
    "TITLE", "PRINCIPAL_PARTS", "PRINCIPAL_PARTS_NO_DIACRITICALS", "SIMPLE_LEMMA",
    "SHORT_DEFINITION", "LONG_DEFINITION", "PART_OF_SPEECH", "LOGEION_LINK",
    "FORCELLINI_LINK", "ROW_FILTERS", "CONJUGATION", "DECLENSION", "PROPER",
    "REGULAR", "STOPWORD", "CORPUSFREQ", "LASLA_Combined"
]

def clean_dictionary_data(df: pd.DataFrame, file_name: str) -> pd.DataFrame:
    df.columns = [col.strip().upper().replace(" ", "_") for col in df.columns]
    missing = [col for col in dictionary_expected_columns if col not in df.columns]
    df["TITLE"] = df["TITLE"].str.upper()
    
    if df[dict_cols_to_check].isnull().any().any():
        null_columns = df.columns[df.isnull().any()]
        update_problematic_texts(file_name, [f"Null values found in dictionary columns: {[col for col in null_columns.tolist() if col in dict_cols_to_check]}."])
        return None

    if missing:
        update_problematic_texts(file_name, [f"Missing expected columns: {missing}"])
        for col in missing:
            df[col] = None
    
    return df[dictionary_expected_columns]

def clean_data(df: pd.DataFrame, file_name: str) -> pd.DataFrame:
    df.columns = map(str.lower, df.columns)
    df = df.rename(columns=lambda x: "".join(x.split(" ")))
    df = df.rename(columns=target_headers)
    df["head_word"] = df["head_word"].str.upper()
    
    cleaned_df = pd.DataFrame(columns=possible_headers)
    # cleaned_df = pd.DataFrame(index=df.index, columns=possible_headers)
    for header in possible_headers:
        if header in df.columns:
            cleaned_df[header] = df[header]

    for header in remove_headers:
        if header in df.columns:
            df = df.drop(header, axis=1)

    for header in df.columns:
        if header not in cleaned_df.columns:
            print(f"Column '{header}' not in target schema. Skipped.")

    if df[text_cols_to_check].isnull().any().any():
        null_columns = df.columns[df.isnull().any()]
        update_problematic_texts(file_name, [f"Null values found in text columns: {[col for col in null_columns.tolist() if col in text_cols_to_check]}."])
        return None
    
    cleaned_df["orthographic_form"] = cleaned_df["orthographic_form"].astype(str)
    
    # Remove trailing .0 from location if it is a float representation
    cleaned_df["location"] = cleaned_df["location"].astype(str).str.replace(r"\.0$", "", regex=True)

    if not good_location_format(file_name, cleaned_df["location"].to_list()):
        return None
    
    if not all_words_in_dictionary(file_name, cleaned_df["head_word"].to_list()):
        return None
    
    return cleaned_df

def all_words_in_dictionary(file_name: str, head_words: list) -> bool:
    if dict_db is None:
        update_problematic_texts(file_name, ["Dictionary database not initialized."])
        return False

    for i, word in enumerate(head_words):
        if word in checked_words: continue
        if not dict_db.find_one({"TITLE": word}):
            update_problematic_texts(file_name, [f"Word '{word}' not found in dictionary. Index: {i}"])
            # return False
        checked_words.add(word)
    return True

def good_location_format(file_name:str, locations: list) -> bool:
    locations = [len(loc.split('_')) for loc in locations]

    if len(set(locations)) == 1:return True
    else:
        update_problematic_texts(file_name, [f"Invalid location format detected, location levels: {set(locations)}"])
        return False

def update_problematic_texts(file_name: str, issues: list):
    if file_name not in problematic_texts:
        problematic_texts[file_name] = []
    problematic_texts[file_name].extend(issues)

def import_dataframe_to_mongo(db: MongoClient, df: pd.DataFrame, collection_name: str, chunk_size: int = 100000):
    if collection_name in db.list_collection_names():
        update_problematic_texts(collection_name, [f"Collection '{collection_name}' already exists. Skipping import."])
        return
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

            try:
                if file_name.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                else:
                    df = pd.read_csv(file_path)
                    
                if database_name.lower() == 'dictionaries':
                    cleaned_df = clean_dictionary_data(df, file_name)
                else:
                    cleaned_df = clean_data(df, file_name)

                if cleaned_df is None or cleaned_df.empty:
                    if file_name not in problematic_texts:
                        problematic_texts[file_name] = ["Invalid data found."]
                    continue
                
                import_dataframe_to_mongo(db, cleaned_df, collection_name)
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
                update_problematic_texts(file_name, [str(e)])
                continue

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
    parser.add_argument("-f", "--folder", required=True, help="Path to folder with Excel/CSV files")
    parser.add_argument("-c", "--collection", required=True, help="Name of the MongoDB collection")
    args = parser.parse_args()

    if not os.path.exists(args.folder):
        print(f"Folder '{args.folder}' does not exist.")
        exit(1)

    if args.collection not in ["Latin-Texts", "Greek-Texts", "dictionaries"]:
        print("Collection name must be either 'Latin-Texts', 'Greek-Texts', or 'dictionaries'.")
        exit(1)
        
    
    mongo_uri = os.getenv('ATLAS_URI')
    print(f"Connecting to MongoDB...")
    if not mongo_uri:
        print("MongoDB URI not found. Ensure you're in the right dir and .env file is set up correctly.")
        exit(1)
        
    database_name = args.collection
    client = MongoClient(mongo_uri)
    db = client[database_name]
    
    if database_name != "dictionaries":
        dict_name = f"bridge_{args.collection.split('-')[0].lower()}_dictionary"
        dict_db = client["dictionaries"][dict_name]

    convert_and_import(f"../data_remediation/{args.folder}", db)
    print("New titles mapping:", new_titles) if args.collection.endswith('-Texts') else print("No new titles mapping for dictionaries.")
    
    if problematic_texts:
        json_path = f"FastBridgeApp/data_remediation/problematic_texts_{database_name}.json"
        with open(f"problematic_texts_{database_name}.json", 'w', encoding='utf-8') as f:
            json.dump(problematic_texts, f, ensure_ascii=False, indent=4)
        print(f"Problematic texts saved to {json_path}")
        
    print("\nData import completed.")