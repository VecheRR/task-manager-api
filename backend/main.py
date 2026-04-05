from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from database import engine, SessionLocal
from models import Task, Base
from sqlalchemy.orm import Session
from schemas import TaskResponse, TaskCreate

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/test-db")
def test_db():
    conn = engine.connect()
    return {"status": "connected"}


@app.post("/tasks", response_model=TaskResponse)
def create_task(taskReq: TaskCreate, db: Session = Depends(get_db)):
    task = Task(title=taskReq.title)

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task


@app.delete("/tasks/{task_id}", response_model=TaskResponse)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")   
    
    db.delete(task)
    db.commit()

    return task


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, taskReq: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.title = taskReq.title  # type: ignore

    db.commit()

    return task