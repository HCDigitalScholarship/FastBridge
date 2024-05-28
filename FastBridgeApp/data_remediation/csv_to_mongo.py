import os
import pandas as pd
#We might not have the packages within this project for these bottom 2 imports, might have to work around that
import json
from subprocess import call

# Define the directory containing CSV files and MongoDB details
csv_directory = '/srv/FastBridge/FastBridgeApp/data_remediation/FOLDERNAME'
mongo_uri = 'mongodb://localhost:27017'
database_name = 'Latin'
collection_name = 'AllTexts'

# Function to convert a CSV file to a JSON object
def csv_to_json(csv_file_path):
    df = pd.read_csv(csv_file_path)
    json_str = df.to_json(orient='records')
    return json.loads(json_str)

# Loop through each CSV file in the directory
for csv_file in os.listdir(csv_directory):
    if csv_file.endswith('.csv'):
        csv_file_path = os.path.join(csv_directory, csv_file)
        json_data = csv_to_json(csv_file_path)

        # Create a temporary JSON file to store the document
        temp_json_file = 'temp.json'
        with open(temp_json_file, 'w') as file:
            json.dump({'filename': csv_file, 'data': json_data}, file)

        # Import the JSON file into MongoDB
        call(['mongoimport', '--uri', mongo_uri, '--db', database_name, '--collection', collection_name, '--file', temp_json_file, '--jsonArray'])

        # Clean up the temporary JSON file
        os.remove(temp_json_file)

print('CSV files imported successfully.')

