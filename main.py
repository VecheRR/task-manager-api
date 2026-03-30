from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import uuid4

app = FastAPI()

tasks = [
    {"id": 1, "title": "Купить молоко"},
    {"id": 2, "title": "Сделать проект"}
]

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return {"error": "Task not found"}

class TaskReq(BaseModel):
    title: str = Field(..., )

class Task(BaseModel):
    id: int
    title: str = Field(..., )

@app.post("/tasks")
def new_task(taskReq: TaskReq):
    task = Task(id=len(tasks) + 1, title=taskReq.title)
    tasks.append(task.model_dump())
    return task