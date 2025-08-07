from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas.task import TaskCreate, TaskUpdate, TaskOut, PaginatedTasks
from ..schemas.error import ErrorResponse
from ..database import SessionLocal
from ..models.task import Task, TaskStatus, TaskPriority
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import os

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication")

@router.get("/", response_model=PaginatedTasks, responses={401: {"model": ErrorResponse}})
def list_tasks(status: Optional[TaskStatus] = None, priority: Optional[TaskPriority] = None, limit: int = 20, offset: int = 0, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    query = db.query(Task).filter(Task.user_id == user_id)
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    total = query.count()
    tasks = query.offset(offset).limit(limit).all()
    return {"tasks": tasks, "pagination": {"total": total, "limit": limit, "offset": offset}}

@router.post("/", response_model=TaskOut, status_code=201, responses={400: {"model": ErrorResponse}})
def create_task(task: TaskCreate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    db_task = Task(**task.dict(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/{id}", response_model=TaskOut, responses={404: {"model": ErrorResponse}})
def get_task(id: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{id}", response_model=TaskOut, responses={400: {"model": ErrorResponse}})
def update_task(id: str, task_update: TaskUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{id}", status_code=204, responses={404: {"model": ErrorResponse}})
def delete_task(id: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return

@router.patch("/{id}/complete", response_model=TaskOut, responses={404: {"model": ErrorResponse}})
def complete_task(id: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = TaskStatus.completed
    db.commit()
    db.refresh(task)
    return task
