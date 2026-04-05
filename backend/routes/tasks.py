from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from models import Task
from schemas import TaskCreate, TaskResponse
import services.task as task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
def create_task(taskReq: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(taskReq, db)


@router.get("/", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return task_service.get_tasks(db)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return task_service.get_task(task_id, db)


@router.delete("/{task_id}", response_model=TaskResponse)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return task_service.delete_task(task_id, db)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, taskReq: TaskCreate, db: Session = Depends(get_db)):
    return task_service.update_task(task_id, taskReq, db)