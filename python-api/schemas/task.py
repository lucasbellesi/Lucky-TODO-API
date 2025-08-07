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
    dueDate: Optional[datetime] = None
    categoryId: Optional[uuid.UUID] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: uuid.UUID
    createdAt: datetime = Field(..., alias="created_at")
    updatedAt: Optional[datetime] = Field(None, alias="updated_at")
    class Config:
        from_attributes = True
        populate_by_name = True

class PaginatedTasks(BaseModel):
    tasks: list[TaskOut]
    pagination: dict
