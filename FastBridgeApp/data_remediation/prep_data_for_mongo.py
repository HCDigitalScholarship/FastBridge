import pandas as pd 
from pathlib import PurePosixPath
import os
import argparse
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest="folder",
        help="current data folder", default="Texts_New")
    options = parser.parse_args()
    convert_to_csv(options.folder)

'''
Standardizes all column labels, removes unwanted columns, and changes current column labels to target column labels   
'''
def clean_data(folder, datasheet, is_csv):
    possible_headers = ["head_word", "location", "section", "orthographic_form", "case", "grammatical_subcategory", "lasla_subordination_code", "local_definition", "local_principal_parts"]
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
        "grammaticalsubcategory": "grammatical_subcategory"
    }

    if is_csv:
        text_data = pd.DataFrame(pd.read_csv(f"../data_remediation/{folder}/{datasheet}"))
    else:
        text_data = pd.DataFrame(pd.read_excel(f"../data_remediation/{folder}/{datasheet}")) 
    
    print("Original columns: ", text_data.columns)
    text_data.columns = map(str.lower, text_data.columns)
    text_data = text_data.rename(columns=lambda x: "".join(x.split(" ")))
    text_data = text_data.rename(columns=target_headers)
    print("Renamed columns: ", text_data.columns) 
    
    text_data_final = pd.DataFrame(columns=possible_headers)

    for header in text_data_final.columns:
        if header in text_data.columns:
            text_data_final[header] = text_data[header].copy()  # This can raise an error if lengths don't match
            text_data = text_data.drop([header], axis=1)

    for header in remove_headers:
        if header in text_data.columns:
            text_data = text_data.drop([header], axis=1)
            print("Removed columns: ", text_data.columns)

    if not text_data.empty:
        for header in text_data.columns:
            if header in text_data_final.columns:  # Check if header exists
                text_data_final[header] = text_data[header].copy()   
            else:
                print(f"Warning: '{header}' not in final columns.")

    return text_data_final


'''
Loops through all text data spreadsheets in local directory and calls data cleaning before converting to a csv file   
'''
def convert_to_csv(folder):
    for root, dirs, files in os.walk(f"../data_remediation/{folder}"):
        for spreadsheet_name in files:
            print("Current text spreadsheet: ", spreadsheet_name)
            if PurePosixPath(spreadsheet_name).suffix == ".csv":
                text_data_final = clean_data(root, spreadsheet_name, True)   
                text_data_final.to_csv(f"Cleaned_Texts/{spreadsheet_name}",  
                                        index=None, 
                                        header=True)
            elif PurePosixPath(spreadsheet_name).suffix == ".xlsx":
                text_data_final = clean_data(root, spreadsheet_name, False)
                spreadsheet_csv_name = spreadsheet_name.strip(".xlsx")    
                text_data_final.to_csv(f"Texts_New_csv/{spreadsheet_csv_name}.csv",  
                                        index=None, 
                                        header=True)
            

if __name__ == "__main__":
    main()
