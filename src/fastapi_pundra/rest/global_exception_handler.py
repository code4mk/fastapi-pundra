import logging
import traceback
from datetime import datetime

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from fastapi_pundra.rest.exceptions import BaseAPIException, MethodNotAllowedException

logger = logging.getLogger("uvicorn.error")


def setup_exception_handlers(app: FastAPI):

    @app.exception_handler(BaseAPIException)
    async def api_exception_handler(request: Request, exc: BaseAPIException):
        error_response = exc.to_dict()
        error_response["path"] = request.url.path
        error_response["type"] = exc.__class__.__name__
        error_response["timestamp"] = datetime.now().isoformat()

        return JSONResponse(
            status_code=exc.status_code,
            content=error_response,
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(request: Request, exc: RequestValidationError):
        errors = {}
        for error in exc.errors():
            loc = error.get("loc", ())
            field = str(loc[-1]) if loc else "unknown"
            msg = error.get("msg", "Invalid value")
            if field not in errors:
                errors[field] = []
            errors[field].append(f"{field} {msg}")

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "success": False,
                "message": "Validation error",
                "errors": errors,
                "path": request.url.path,
                "type": "RequestValidationError",
                "timestamp": datetime.now().isoformat(),
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.detail,
                "path": request.url.path,
                "type": "HTTPException",
                "timestamp": datetime.now().isoformat(),
            },
        )

    def _build_api_error_response(request: Request, exc: BaseAPIException) -> JSONResponse:
        error_response = exc.to_dict()
        error_response["path"] = request.url.path
        error_response["type"] = exc.__class__.__name__
        error_response["timestamp"] = datetime.now().isoformat()
        return JSONResponse(status_code=exc.status_code, content=error_response)

    @app.middleware("http")
    async def exception_handling_middleware(request: Request, call_next):
        try:
            response = await call_next(request)

            if response.status_code == 405:
                raise MethodNotAllowedException(message="Method not allowed")

            return response
        except BaseAPIException as exc:
            return _build_api_error_response(request, exc)
        except Exception as exc:
            logger.error(
                "Unhandled exception on %s %s\n%s",
                request.method,
                request.url.path,
                traceback.format_exc(),
            )

            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "Internal server error",
                    "type": exc.__class__.__name__,
                    "path": request.url.path,
                    "timestamp": datetime.now().isoformat(),
                },
            )
