from pymongo import MongoClient


client = MongoClient("mongodb+srv://root:omusi,2025@cluster0.3lgpw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.todo_db
collection_name = db["todo_collections"]