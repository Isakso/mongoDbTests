# json Serializer

from models import todos


# function to serialize the items
def list_serialize_todo_item(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "title": todo["title"],
        "description": todo.get("description", ""),
        "completed": todo["completed"],
        "day": todo["day"]
    }


# deserialiser
def list_serialize_todo_item(todos) -> list:
    return [list_serialize_todo_item(todo) for todo in todos]
