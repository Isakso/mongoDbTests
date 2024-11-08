from email import errors
from dotenv import load_dotenv

from motor.motor_asyncio import AsyncIOMotorClient

import os




load_dotenv()

username = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")
db_name = os.getenv("MONGO_DB_NAME")
collection_name_str = os.getenv("MONGO_COLLECTION_NAME")


try:

    client = AsyncIOMotorClient(f"mongodb+srv://{username}:{password}@cluster0.3lgpw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client[db_name]
    collection_name = db[collection_name_str]
    print("Connected to the database successfully!")
except Exception as e:
    print(f"Could not connect to the database: {e}")
