from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()

#Connect to Mongo Atlas Cluster
mongo_client = MongoClient(os.getenv("MONGO_URI"))


# Access database
dummy_user_db = mongo_client["dummy_user_db"]


# Pick a connection to operate on
user_collection = dummy_user_db["user"]
