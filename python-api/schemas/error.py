from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from datetime import datetime

class ErrorDetail(BaseModel):
    code: str = Field(..., example="VALIDATION_ERROR")
    message: str = Field(..., example="Invalid request data")
    details: Optional[Dict[str, List[str]]] = None

class ErrorResponse(BaseModel):
    error: ErrorDetail
    timestamp: Optional[datetime]
    path: Optional[str]
