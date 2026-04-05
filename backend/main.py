from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from database import engine, SessionLocal
from models import Task, Base
from sqlalchemy.orm import Session
from schemas import TaskResponse, TaskCreate
from routes.tasks import router as task_router

app = FastAPI()

app.include_router(task_router)

Base.metadata.create_all(bind=engine)