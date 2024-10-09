from fastapi import APIRouter
from models.todos import Todos
from config.database import collection_name
from bson import ObjectId

from schema.schema import list_serial

router = APIRouter()


@router.get("/")
async def get_todo():
    todos = list_serial(collection_name.find())
    return todos


@router.post("/")
async def post_todo(todo: Todos):
    collection_name.insert_one(dict.find)

