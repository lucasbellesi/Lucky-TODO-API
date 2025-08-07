from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from schemas.error import ErrorDetail, ErrorResponse
from datetime import datetime

# Add error handlers to FastAPI app
def add_error_handlers(app: FastAPI):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        err = ErrorResponse(
            error=ErrorDetail(
                code="HTTP_ERROR",
                message=exc.detail,
                details=None
            ),
            timestamp=datetime.utcnow(),
            path=str(request.url.path)
        )
        return JSONResponse(status_code=exc.status_code, content=err.dict())

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        err = ErrorResponse(
            error=ErrorDetail(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred.",
                details=None
            ),
            timestamp=datetime.utcnow(),
            path=str(request.url.path)
        )
        return JSONResponse(status_code=500, content=err.dict())
