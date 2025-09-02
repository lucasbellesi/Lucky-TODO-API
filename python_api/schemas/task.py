from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
import uuid
from datetime import datetime
from ..models.task import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[TaskStatus] = TaskStatus.pending
    priority: Optional[TaskPriority] = TaskPriority.medium
    # Use snake_case attribute names with camelCase aliases for IO
    due_date: Optional[datetime] = Field(
        None, serialization_alias="dueDate", validation_alias="dueDate"
    )
    category_id: Optional[uuid.UUID] = Field(
        None, serialization_alias="categoryId", validation_alias="categoryId"
    )


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = Field(
        None, serialization_alias="dueDate", validation_alias="dueDate"
    )
    category_id: Optional[uuid.UUID] = Field(
        None, serialization_alias="categoryId", validation_alias="categoryId"
    )


class TaskOut(TaskBase):
    id: uuid.UUID
    createdAt: datetime = Field(..., alias="created_at")
    updatedAt: Optional[datetime] = Field(None, alias="updated_at")
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PaginatedTasks(BaseModel):
    tasks: list[TaskOut]
    pagination: dict
