from fastapi import APIRouter, HTTPException
from typing import List
from models.todos import Todos
from config.database import collection_name
from bson import ObjectId
from schema.schema import list_serialize_todo_item, list_serial

router = APIRouter()

# Retrieve all todos
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


# Retrieve a task by id
@router.get("/{todo_id}", response_model=Todos)
async def get_todo_by_id(todo_id: str):
    try:
        print(f"Received todo_id: {todo_id}")
        todo_id = todo_id.strip().replace("'", "").replace('"', "")
        # Convert the todo_id string to an ObjectId
        todo_object_id = ObjectId(todo_id)
        print(f"Converted ObjectId: {todo_object_id}")

        # Fetch from collection
        todo_data = collection_name.find_one({"_id": todo_object_id})
        print(f"Fetched Todo Data: {todo_data}")

        if todo_data is None:
            raise HTTPException(status_code=404, detail="Todo not found")

        # Return the serialized item
        return list_serialize_todo_item(todo_data)

    except Exception as e:
        # Handle errors gracefully and raise a 500 HTTPException
        print(f"Error occurred while fetching todo by id: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch todo")


# Create a new task
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


# Create multiple todos
@router.post("/multiple")
async def create_multiple_todos(todos: List[Todos]):
    try:
        #  insert multiple todos into the collection
        new_todos = [todo.dict(exclude_unset=True, exclude={"id"}) for todo in todos]
        result = collection_name.insert_many(new_todos)

        if not result.inserted_ids:
            raise HTTPException(status_code=500, detail="Failed to create multiple todo items")

        # Fetch and serialize inserted todos
        inserted_todos = collection_name.find({"_id": {"$in": result.inserted_ids}})
        return [list_serialize_todo_item(todo) for todo in inserted_todos]

    except Exception as e:
        print(f"Error occurred while adding multiple todos: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create multiple todos")
