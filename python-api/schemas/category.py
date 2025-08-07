from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    color: Optional[str] = Field(None, pattern=r'^#[0-9a-fA-F]{6}$')

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: uuid.UUID
    createdAt: datetime
    updatedAt: Optional[datetime]
    class Config:
        from_attributes = True
