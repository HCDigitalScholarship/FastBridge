import os
import pandas as pd
#We might not have the packages within this project for these bottom 2 imports, might have to work around that
import json
from subprocess import call
import sys
import json

# Define the directory containing CSV files and MongoDB details
csv_directory = '/srv/FastBridge/FastBridgeApp/data_remediation/Cleaned_FastBridge_Files_SAMPLE'
mongo_uri = 'mongodb://localhost:27017'
database_name = 'Latin'

# Function to convert a CSV file to a JSON object
def csv_to_json(csv_file_path):
    df = pd.read_csv(csv_file_path)
    json_str = df.to_json(orient='records')

    # Check the size of the JSON object in memory
    json_size_in_memory = sys.getsizeof(json_str) / (1024 * 1024)
    if json_size_in_memory > 16:
        print("Warning: The size of the JSON object in memory exceeds 16MB")
        print(f"Size of JSON object: {json_size_in_memory:.2f} MB")

    return json.loads(json_str)

# Loop through each CSV file in the directory
for csv_file in os.listdir(csv_directory):
    if csv_file.endswith('.csv'):
        # Get path to CSV file
        csv_file_path = os.path.join(csv_directory, csv_file)
        print(str(csv_file_path)+"\n")
        json_data = csv_to_json(csv_file_path)

        # Strip the .csv extension from the file name
        collection_name = os.path.splitext(csv_file)[0]

        # Create a temporary JSON file to store the document
        temp_json_file = 'temp.json'
        with open(temp_json_file, 'w') as file:
            json.dump([{'filename': csv_file, 'data': json_data}], file)

        # Import the JSON file into MongoDB
        call(['mongoimport', '--uri', mongo_uri, '--db', database_name, '--collection', collection_name, '--file', temp_json_file, '--jsonArray'])
        print("adding .json file as a document to ", database_name)

        # Clean up the temporary JSON file
        os.remove(temp_json_file)

print('CSV files imported successfully.')

