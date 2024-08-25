from pymongo import MongoClient
import json

# Connect to MongoDB

HOST = 'localhost'
PORT = 27017
DB = 'rrn'
COL = 'novels'

client = MongoClient('mongodb://%s:%d' % (HOST,PORT))
db = client['%s' % (DB)]
collection = db['%s' % (COL)]

# Load the .json file
try:
    with open('royalRoadNovels1.json') as file:
        data = json.load(file)
    
    # Insert the data into the collection
    if isinstance(data, list):
        # If the data is a list of documents
        collection.insert_many(data)
    else:
        # If the data is a single document
        collection.insert_one(data)

    print("Insertion Successful")

except Exception as e:
    print("Insertion not Successful: {}".format(e))