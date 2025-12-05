from typing import Literal

from pydantic import BaseModel


class Action(BaseModel):
    type: Literal["task", "note"]
