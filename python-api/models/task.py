from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
import uuid
import enum

class TaskStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"

class TaskPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.pending, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.medium, nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    category_id = Column(String, ForeignKey("categories.id"), nullable=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    category = relationship("Category", back_populates="tasks")
    user = relationship("User", back_populates="tasks")
