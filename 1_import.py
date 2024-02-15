from dotenv import load_dotenv
import os
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import glob

# Load environment variables from local .env file
load_dotenv()

# Directory containing JSON files
directory_path = './data/data_in_json'

# Create a new client and connect to the server
client = MongoClient(os.getenv('MONGODB_URI'), server_api=ServerApi('1'))
db = client[os.getenv("MONGODB_DATABASE")]
collection = db[os.getenv("MONGODB_COLLECTION")]

# Loop through each JSON file in the directory
for json_file in glob.glob(os.path.join(directory_path, '*.json')):
    with open(json_file, 'r') as f:
        data = json.load(f)  # Load the data from the JSON file

        # Check if data is a list of documents
        if isinstance(data, list):
            collection.insert_many(data)  # Insert list of documents
        else:
            collection.insert_one(data)  # Insert a single document

print("All files have been uploaded.")
