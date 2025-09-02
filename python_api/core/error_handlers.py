from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from ..schemas.error import ErrorDetail, ErrorResponse
from datetime import datetime, timezone


def add_error_handlers(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # Transform list of validation errors into { field: [messages] }
        details = {}
        try:
            for err in exc.errors():
                loc = err.get("loc", [])
                # Ignore the first segment like 'body', 'query', etc.
                key_parts = [str(p) for p in loc[1:]] if len(loc) > 1 else [str(loc[0])] if loc else ["__root__"]
                key = ".".join(key_parts)
                details.setdefault(key, []).append(err.get("msg", "Invalid value"))
        except Exception:
            details = None

        err = ErrorResponse(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="Invalid request data",
                details=details,
            ),
            timestamp=datetime.now(timezone.utc),
            path=str(request.url.path),
        )
        return JSONResponse(status_code=422, content=jsonable_encoder(err))
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
