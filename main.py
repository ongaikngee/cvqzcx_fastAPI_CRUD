from typing import List

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class TodoBase(BaseModel):
    name: str
    descriptions: str


class Todo(TodoBase):
    id: int


all_todos: List[dict] = [
    {"id": 1, "name": "Sports", "descriptions": "Go to the gym"},
    {"id": 2, "name": "Groceries", "descriptions": "Buy milk and eggs"},
    {"id": 3, "name": "Work", "descriptions": "Finish the report"},
    {"id": 4, "name": "Reading", "descriptions": "Read 30 pages"},
    {"id": 5, "name": "Call", "descriptions": "Call mom"},
    {"id": 6, "name": "Cleanup", "descriptions": "Clean the kitchen"},
]


def _next_id() -> int:
    return max((t["id"] for t in all_todos), default=0) + 1


@app.get("/", response_model=List[Todo])
def read_root():
    return all_todos


@app.get("/todos", response_model=List[Todo])
def get_todos():
    return all_todos


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoBase):
    new = payload.dict()
    new["id"] = _next_id()
    all_todos.append(new)
    return new


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, payload: TodoBase):
    for idx, todo in enumerate(all_todos):
        if todo["id"] == todo_id:
            all_todos[idx]["name"] = payload.name
            all_todos[idx]["descriptions"] = payload.descriptions
            return all_todos[idx]
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    for idx, todo in enumerate(all_todos):
        if todo["id"] == todo_id:
            del all_todos[idx]
            return
    raise HTTPException(status_code=404, detail="Todo not found")