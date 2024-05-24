import pandas as pd 
import os

def main():
    convert_to_csv()

'''
Standardizes all column labels, removes unwanted columns, and changes current column labels to target column labels   
'''
def clean_data(folder, datasheet):

    possible_headers = ["HEAD_WORD", "LOCATION", "SECTION", "ORTHOGRAPHIC_FORM", "CASE", "GRAMMATICAL_SUBCATEGORY", "LASLA_SUBORDINATION_CODE", "LOCAL_DEFINITION", "LOCAL_PRINCIPAL_PARTS"]
    remove_headers = ["GRAMMATICAL_CATEGORY", "_MERGE"]
    target_headers = {"TITLE": "HEAD_WORD", "TEXT": "ORTHOGRAPHIC_FORM", "SUBORDINATION_CODE": "LASLA_SUBORDINATION_CODE", "LOCALDEF": "LOCAL_DEFINITION", "LOCAL DEFINITION": "LOCAL_DEFINITION", "RUNNINGCOUNT": "COUNTER", "GRAMMATICAL_CATEGORY_SUB": "GRAMMATICAL_SUBCATEGORY"}

    text_data = pd.DataFrame(pd.read_excel(f"../data_remediation/Texts_New/{folder}/{datasheet}")) 
    
    print("Original columns: ", text_data.columns)
    text_data = text_data.rename(columns=target_headers)
    text_data.columns = map(str.upper, text_data.columns)
    print("Renamed columns: ", text_data) 
    
    text_data_final = pd.DataFrame(columns=possible_headers)

    for header in text_data_final.columns:
        if header in text_data.columns:
            text_data_final[header] = text_data[header].copy()
            text_data = text_data.drop([header], axis=1)

    for header in remove_headers:
        if header in text_data.columns:
            text_data = text_data.drop([header], axis=1)
            print("Removed columns: ", text_data.columns)

    if not text_data.empty:
        for header in text_data.columns:
            text_data_final[header] = text_data[[header]].copy()   

    print("Final columns: ", text_data_final)

    return text_data_final

'''
Loops through all text data spreadsheets in local directory and calls data cleaning before converting to a csv file   
'''
def convert_to_csv():
    for folder in os.listdir("../data_remediation/Texts_New/"):
        for spreadsheet_name in os.listdir(f"../data_remediation/Texts_New/{folder}"):
            
            print("Current text spreadsheet: ", spreadsheet_name)

            text_data_final = clean_data(folder, spreadsheet_name)
            
            spreadsheet_csv_name = spreadsheet_name.strip(".xlsx")        
            text_data_final.to_csv (f"Texts_New_csv/{spreadsheet_csv_name}.csv",  
                    index = None, 
                    header=True)
                    

if __name__ == "__main__":
    main()
