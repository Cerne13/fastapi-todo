from pydantic import BaseModel, Field


class Todo(BaseModel):
    title: str
    description: str | None = None
    priority: int = Field(ge=1, le=10, description='Priority must be from 1 to 10')
    complete: bool = Field(default=False)


class TodoList(BaseModel):
    total: int
    todos: list[Todo]