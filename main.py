from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

next_id = 1

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
    raise HTTPException(status_code=404, detail="Task not found")

class TaskReq(BaseModel):
    title: str = Field(..., )

class Task(BaseModel):
    id: int
    title: str = Field(..., )

@app.post("/tasks", status_code=201)
def new_task(taskReq: TaskReq):
    global next_id
    task = Task(id=next_id, title=taskReq.title)
    next_id += 1
    tasks.append(task.model_dump())
    return task

@app.delete("/tasks/{task_id}")
def del_task(task_id: int):
    for i in range(len(tasks)):
        if tasks[i]["id"] == task_id:
            del tasks[i]
            return {"message": "Task deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Task not found")