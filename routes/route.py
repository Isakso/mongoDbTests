from fastapi import APIRouter, HTTPException, logger
from typing import List
from models.todos import Todos
from config.database import collection_name
from bson import ObjectId
from schema.schema import list_serial

router = APIRouter()


def list_serial(cursor):
    todos_list = []
    for document in cursor:
        todos_list.append(Todos(**document))
    return todos_list


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


@router.get("/{todo_id}", response_model=Todos)
async def get_todo_by_id(todo_id: str):
    try:
        # Convert the todo_id string to an ObjectId
        todo_object_id = ObjectId(todo_id)

        #fetch from collection
        todo_data = await collection_name.find_one({"_id": todo_object_id})

        if todo_data is None:

            raise HTTPException(status_code=404, detail="Todo not found")

        # Create a Todos instance from the fetched data
        todo = Todos(**todo_data)
        return todo

    except Exception as e:
        logger.error(f"Error occurred while fetching todo by id: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch todo")


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
