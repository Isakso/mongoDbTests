#json Serializer
from models import todos


def individual_serial(todo)->dict:
    return {"id":str(todo["_id"]),
            "name":todo["_name"],
            "description":todo["_description"],
            "complete":todo["complete"]

    }
#deserialiser
def list_serial(todo)->list:
    return [individual_serial(todo) for todo in todos]