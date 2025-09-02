from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from datetime import datetime

class ErrorDetail(BaseModel):
    code: str = Field(..., json_schema_extra={"example": "VALIDATION_ERROR"})
    message: str = Field(..., json_schema_extra={"example": "Invalid request data"})
    details: Optional[Dict[str, List[str]]] = None

class ErrorResponse(BaseModel):
    error: ErrorDetail
    timestamp: Optional[datetime]
    path: Optional[str]
