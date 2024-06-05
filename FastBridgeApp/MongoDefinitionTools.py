#Meant to be a copy of DefinitionTools but with Mongo queries instead of data/*.py queries
#Currently running a local MongoDB deployment on dev droplet

from pymongo import MongoClient

try:
    # start connection code heri

    uri = "mongodb://localhost:27017/"
    client = MongoClient(uri)

    # end connection code here
    client.admin.command("ping")
    print("Connected successfully")
    # other application code
    client.close()
except Exception as e:
    raise Exception(
        "The following error occurred: ", e)



