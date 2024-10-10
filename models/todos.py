from typing import Optional

from pydantic import BaseModel, Field


class Todos(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name:str
    description: str
    complete:bool




