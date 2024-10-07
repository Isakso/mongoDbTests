from pydantic import BaseModel

class Todos(BaseModel):
    name:str
    description: str
    complete:bool
    


