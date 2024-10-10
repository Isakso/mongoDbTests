from fastapi import APIRouter, HTTPException
from typing import List
from models.todos import Todos
from config.database import collection_name
from bson import ObjectId
from schema.schema import list_serial

router = APIRouter()

# GET: Retrieve all todos
@router.get("/", response_model=List[Todos])
async def get_todo():
    try:
        todos_cursor = collection_name.find()  # Fetch all todos from MongoDB
        todos = list_serial(todos_cursor)
        return todos
    except Exception as e:
        # Log the exception for debugging
        print(f"Error occurred while fetching todos: {str(e)}")
        # Raise an HTTP exception with a descriptive message
        raise HTTPException(status_code=500, detail="Failed to fetch todos")

@router.post("/")
async def post_todo(todo: Todos):
    try:

        new_todo = todo.dict(exclude_unset=True, exclude={"id"})
        result = collection_name.insert_one(new_todo)

        return {"message": "Todo added successfully", "id": str(result.inserted_id)}
    except Exception as e:
        # Log the exception for debugging
        print(f"Error occurred while adding todo: {str(e)}")
        # Raise an HTTP exception with a descriptive message
        raise HTTPException(status_code=500, detail=str(e))
