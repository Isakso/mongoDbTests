from typing import List

from pydantic import BaseModel

from models.DayOfWeek import DayOfWeek
from models.todos import Todos


class DaySchedlue(BaseModel):
    day: DayOfWeek
    todos: List[Todos] = []
