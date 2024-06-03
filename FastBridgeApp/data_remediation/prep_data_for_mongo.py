import pandas as pd 
from pathlib import PurePosixPath
import os
import argparse
import numpy as np

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest="data_folder",
        help="current data folder", default="Texts_New")
    parser.add_argument("-d", dest="data_type",
        help="specify text or dictionary data", default="text")
    options = parser.parse_args()
    convert_to_csv(options.data_folder, options.data_type)


'''
Loops through all text data spreadsheets in local directory and calls data cleaning before converting to a csv file (if not already a csv file) 
'''
def convert_to_csv(data_folder, data_type):
    if data_type == "text":
        is_text_data = True
    elif data_type == "dict" or data_type == "dictionary":
        is_text_data = False
    else:
        raise argparse.ArgumentTypeError('Invalid value!')
    acceptable_headers, target_headers, necessary_headers = data_config(is_text_data)
    
    for spreadsheet_name in os.listdir(f"../data_remediation/{data_folder}"):
        print("Current Spreadsheet: ", spreadsheet_name)
    
        if PurePosixPath(spreadsheet_name).suffix == ".csv":
            data = pd.DataFrame(pd.read_csv(f"../data_remediation/{data_folder}/{spreadsheet_name}"))
            cleaned_data_final = clean_data(data, spreadsheet_name, acceptable_headers, target_headers, necessary_headers, is_text_data)   
            cleaned_data_final.to_csv(f"Cleaned_Texts/{spreadsheet_name}",  
                index = None, 
                header=True)
        else:
            data = pd.DataFrame(pd.read_excel(f"../data_remediation/{data_folder}/{spreadsheet_name}")) 
            cleaned_data_final = clean_data(data, spreadsheet_name, acceptable_headers, target_headers, necessary_headers, is_text_data)
            spreadsheet_csv_name = spreadsheet_name.strip(".xlsx")    
            cleaned_data_final.to_csv(f"Texts_New_csv/{spreadsheet_csv_name}.csv",  
                index = None, 
                header=True)
                

'''
Assigns acceptable and target headers for data to be compared against 
'''
def data_config(is_text_data):
    necessary_headers = ["head_word", "location", "section", "counter", "orthographic_form"]
    if is_text_data:
        data_acceptable_headers = ["head_word", "location", "section", "counter", "orthographic_form", "case", "grammatical_subcategory", "lasla_subordination_code", "local_definition", "local_principal_parts"]
        data_target_headers = {
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
                    "grammaticalsubcategory": "grammatical_subcategory"}
        return data_acceptable_headers, data_target_headers, necessary_headers
    else:
        dict_data_acceptable_headers = ["head_word", "lilaLemma", "principal_parts", "principal_parts_no_diacriticals", "simple_lemma", "gloss", "definition", "local_definition", "part_of_speech", 
                                        "logeion_link", "forcellini_link", "conjugation", "declension", "proper", "regular", "stopword", "corpus_freq", "lasla_combined"]
        dict_data_target_headers = {
                    "title": "head_word", 
                    "headword": "head_word", 
                    "short_definition": "gloss",
                    "shortdefinition": "gloss",
                    "long_definition": "definition",
                    "longdefinition": "definition",
                    "local_principal_parts": "principal_parts"}
        return dict_data_acceptable_headers, dict_data_target_headers, necessary_headers
            

'''
Standardizes all column labels, removes unwanted columns, and changes current column labels to target column labels   
'''
def clean_data(data, datasheet, acceptable_headers, target_headers, necessary_headers, is_text_data):

    print("Original Columns:\n", data.columns)
    data.columns = map(str.lower, data.columns)
    data = data.rename(columns=lambda x: x.rstrip())
    data = data.rename(columns=lambda x: x.replace(" ", "_"))
    data = data.rename(columns=target_headers)
    print("Renamed columns:\n", data.columns) 
    
    cleaned_data_final = pd.DataFrame(columns=necessary_headers)

    cleaned_data = check_for_duplicates(datasheet, data)

    if not is_text_data and "principal_parts" in cleaned_data.columns:
        cleaned_data = add_no_diacriticals_column(cleaned_data)

    for header in cleaned_data_final.columns:
        if header in cleaned_data.columns:
            cleaned_data_final[header] = cleaned_data[header].copy()

    for header in cleaned_data.columns:
        if header in acceptable_headers:
            cleaned_data_final[header] = cleaned_data[[header]].copy()
        
    print("Final columns:\n", cleaned_data_final)

    return cleaned_data_final

'''
Checks for both column duplicates and row duplicates (as well as entire rows/columns with NaN values), removes them, and logs them in the folder duplicate_data
'''
def check_for_duplicates(spreadsheet_name, data):
    column_header_duplicates = data.columns.duplicated(keep=False)
    if column_header_duplicates.any():
        duplicate_columns = data.iloc[:, column_header_duplicates]
        print("Duplicate Columns:\n", duplicate_columns)
        if not os.path.exists(f"../data_remediation/duplicate_data/"):
            os.mkdir(f"../data_remediation/duplicate_data/")
        if not os.path.exists(f"../data_remediation/duplicate_data/duplicate_columns/"):
            os.mkdir(f"../data_remediation/duplicate_data/duplicate_columns/")
        spreadsheet_csv_name = spreadsheet_name.strip(".xlsx")
        f = open(f"duplicate_data/duplicate_columns/{spreadsheet_csv_name}.csv", "w")
        f.write(f"{spreadsheet_csv_name}\n")
        f.write(duplicate_columns.to_csv(na_rep="NaN", index=False))
        f.close()
        data = data.dropna(axis=1, how="all")
        dropped_columns = [col for col in data if col not in data.columns]
        print("Dropped Columns: ", dropped_columns)

    row_duplicates = data.duplicated(keep=False)
    if row_duplicates.any():
        duplicate_rows = data[row_duplicates]
        print("Duplicate Rows: ", duplicate_rows)
        if not os.path.exists(f"../data_remediation/duplicate_data/"):
            os.mkdir(f"../data_remediation/duplicate_data/")
        if not os.path.exists(f"../data_remediation/duplicate_data/duplicate_rows/"):
            os.mkdir(f"../data_remediation/duplicate_data/duplicate_rows/")
        spreadsheet_csv_name = spreadsheet_name.strip(".xlsx")
        f = open(f"duplicate_data/duplicate_rows/{spreadsheet_csv_name}.csv", "w")
        f.write(f"{spreadsheet_csv_name}\n")
        f.write(duplicate_rows.to_csv(na_rep="NaN"))
        f.close()
        data = data.drop_duplicates()
    
    return data


def add_no_diacriticals_column(data):
    no_diacriticals = []
    for row in data["principal_parts"]:
        replaced_diacriticals = row.replace("ā","a").replace("ē","e").replace("ī","i").replace("ō","o").replace("ū","u").replace("ȳ","y").replace("Ā","A").replace("Ē","E").replace("Ī","I").replace("Ō","O").replace("Ū","U").replace("ë","e")
        no_diacriticals.append(replaced_diacriticals)
    data = data.assign(principal_parts_no_diacriticals=no_diacriticals)
    return data

if __name__ == "__main__":
    main()
