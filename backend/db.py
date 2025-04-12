from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))

db = client["secureshare"] 

users_collection = db["users"]
files_collection = db["files"]
logs_collection = db["logs"]
