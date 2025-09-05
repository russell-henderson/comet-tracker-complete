# backend/check_db.py
import os
from pymongo import MongoClient
from pprint import pformat

mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
db_name = os.getenv("DB_NAME", "comet_tracker")

client = MongoClient(mongo_url, serverSelectionTimeoutMS=3000)
db = client[db_name]

count = db.comet_data.count_documents({})
print(f"comet_data.count_documents: {count}")

print("\nLatest 3 docs:")
for doc in db.comet_data.find().sort("ts", -1).limit(3):
    print(pformat(doc))
