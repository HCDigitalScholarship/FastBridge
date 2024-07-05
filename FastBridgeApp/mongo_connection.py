from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

try:
    # Use the environment variable for the MongoDB URI
    uri = 'mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.10'

    # Create a MongoClient with the URI containing authentication details
    client = MongoClient(uri)

    # Check if the connection is successful
    client.admin.command("ping")
    print("Connected successfully to MongoDB")

    db = client.get_database("Latin")  # This will use the database specified in the URI
    dict_db = client.get_database("Latin-Dicts")
    print("Connected to database:", db.name)

except ConnectionFailure as e:
    print(f"Failed to connect to MongoDB: {e}")
    raise
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    raise



