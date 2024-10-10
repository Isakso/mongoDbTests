# json Serializer

from models import todos


def individual_serial(todo) -> dict:
    return {"id": str(todo["_id"]),
            "name": todo["name"],
            "description": todo["description"],
            "complete": todo["complete"]

            }


# deserialiser
def list_serial(todos) -> list:
    return [individual_serial(todo) for todo in todos]
