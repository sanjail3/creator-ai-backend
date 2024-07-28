from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("Mongodb_url")
client = MongoClient(url,server_api=ServerApi('1'))
try:
    client = client["ai_video_creator"]
    print("Connected to MongoDB")
except Exception as e:
    print("Connection failed", e)