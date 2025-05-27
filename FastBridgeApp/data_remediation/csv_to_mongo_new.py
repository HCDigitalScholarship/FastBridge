import os
import pandas as pd
import json
from subprocess import call
import sys

# Define the directory containing CSV files and MongoDB details
csv_directory = 'fill_in'
mongo_uri = 'mongodb://localhost:27017'
database_name = 'Latin'

# Function to convert a CSV file chunk to a JSON object
def csv_chunk_to_json(chunk):
    json_str = chunk.to_json(orient='records')
    return json.loads(json_str)

# Function to import JSON chunks into MongoDB
def import_json_chunks(json_chunks, collection_name):
    for i, chunk in enumerate(json_chunks):
        temp_json_file = f'temp_{i}.json'

        temp_json_file_size = sys.getsizeof(temp_json_file) / (1024 * 1024)
        if temp_json_file_size > 16:
            print("Warning: The size of the JSON object in memory exceeds 16MB")
            sys.exit("Stopping the program")
        
        with open(temp_json_file, 'w') as file:
            json.dump(chunk, file)
        
        # Import the JSON file into MongoDB
        call(['mongoimport', '--uri', mongo_uri, '--db', database_name, '--collection', collection_name, '--file', temp_json_file, '--jsonArray'])
        
        # Clean up the temporary JSON file
        os.remove(temp_json_file)
        print(f"Chunk {i+1}/{len(json_chunks)} of {collection_name} imported successfully.")

# Loop through each CSV file in the directory
for csv_file in os.listdir(csv_directory):
    if csv_file.endswith('.csv'):
        # Get path to CSV file
        csv_file_path = os.path.join(csv_directory, csv_file)
        print(f"Processing file: {csv_file_path}\n")
        
        # Read the CSV file in chunks
        chunk_size = 100_000  # Adjust the chunk size as needed, chunk_size = # rows
        json_chunks = []
        for chunk in pd.read_csv(csv_file_path, chunksize=chunk_size):
            json_chunk = csv_chunk_to_json(chunk)
            json_chunks.append(json_chunk)
        
        # Strip the .csv extension from the file name
        collection_name = os.path.splitext(csv_file)[0]
        
        # Import JSON chunks into MongoDB
        import_json_chunks(json_chunks, collection_name)

print('CSV files imported successfully. With chunk size ' + str(chunk_size))