from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarletteHTTPException
from ..schemas.error import ErrorDetail, ErrorResponse
from datetime import datetime, timezone


def add_error_handlers(app: FastAPI):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        err = ErrorResponse(
            error=ErrorDetail(
                code="HTTP_ERROR",
                message=exc.detail,
                details=None,
            ),
            timestamp=datetime.now(timezone.utc),
            path=str(request.url.path),
        )
        return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(err))

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        err = ErrorResponse(
            error=ErrorDetail(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred.",
                details=None,
            ),
            timestamp=datetime.now(timezone.utc),
            path=str(request.url.path),
        )
        return JSONResponse(status_code=500, content=jsonable_encoder(err))

