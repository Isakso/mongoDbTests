from typing import Any, Dict

# serialize a single todo item
def list_serialize_todo_item(todo: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": str(todo.get("_id")) if "_id" in todo else None,  # Convert ObjectId to string if present
        "name": todo.get("name", ""),                            # Default to empty string if name is missing
        "description": todo.get("description", ""),   
        "day": todo.get("day", ""),          
        "complete": todo.get("complete", False)               
    }

# serialize a list of todos using the provided cursor
async def list_serial(cursor) -> list:
    # Await the cursor to list conversion
    todos_list = await cursor.to_list(length=None)
    # Return serialized list of todos
    return [list_serialize_todo_item(todo) for todo in todos_list]


