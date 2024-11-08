# json Serializer

from models import todos


# function to serialize the items
def list_serialize_todo_item(todo: dict) -> dict:
    return {
        "id": str(todo.get("_id")),
        "name": todo.get("name", ""),
        "description": todo.get("description", ""),
        "complete": todo.get("complete", False),
        "day": todo.get("day", "")
    }


# deserializer
def list_serial(cursor) -> list:
    todos_list = list(cursor)  #
    return [list_serialize_todo_item(todo) for todo in todos_list]
