from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
import uuid
from datetime import datetime

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    color: Optional[str] = Field(None, pattern=r'^#[0-9a-fA-F]{6}$')

class CategoryCreate(CategoryBase):
    pass

from pydantic import computed_field

class CategoryOut(CategoryBase):
    id: uuid.UUID
    createdAt: datetime = Field(..., alias="created_at")
    updatedAt: Optional[datetime] = Field(None, alias="updated_at")
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
