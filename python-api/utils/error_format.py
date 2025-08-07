from fastapi import Request
from fastapi.responses import JSONResponse
from schemas.error import ErrorDetail, ErrorResponse
from datetime import datetime

def format_error(code: str, message: str, details: dict = None, path: str = None):
    return ErrorResponse(
        error=ErrorDetail(code=code, message=message, details=details),
        timestamp=datetime.utcnow(),
        path=path
    )

def error_response(status_code: int, code: str, message: str, details: dict = None, path: str = None):
    err = format_error(code, message, details, path)
    return JSONResponse(status_code=status_code, content=err.dict())
