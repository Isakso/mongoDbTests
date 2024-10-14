from pymongo import MongoClient, errors

try:
    client = MongoClient("mongodb+srv://root:****@cluster0.3lgpw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client.todo_db
    collection_name = db["todo_collections"]
    print("Connected to the database successfully!")
except errors.ConnectionError as e:
    print(f"Could not connect to the database: {e}")