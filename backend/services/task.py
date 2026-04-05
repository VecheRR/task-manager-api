from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from models import Task
from schemas import TaskCreate, TaskResponse

def create_task(taskReq: TaskCreate, db: Session = Depends(get_db)):
    task = Task(title=taskReq.title)

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks


def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task


def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")   
    
    db.delete(task)
    db.commit()

    return task


def update_task(task_id: int, taskReq: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.title = taskReq.title  # type: ignore

    db.commit()

    return task