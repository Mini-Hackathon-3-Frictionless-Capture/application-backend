from pydantic import BaseModel


class ActionableTask(BaseModel):
    title: str
    content: str | None = None
    due_date: str | None = None
