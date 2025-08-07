from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    pending = "pending"
    completed = "completed"

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[TaskStatus] = TaskStatus.pending
    priority: Optional[TaskPriority] = TaskPriority.medium
    dueDate: Optional[datetime]
    categoryId: Optional[uuid.UUID]

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: uuid.UUID
    createdAt: datetime
    updatedAt: Optional[datetime]
    class Config:
        from_attributes = True

class PaginatedTasks(BaseModel):
    tasks: list[TaskOut]
    pagination: dict
