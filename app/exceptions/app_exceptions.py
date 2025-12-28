import uuid
from fastapi import HTTPException, Request
from fastapi.responses import ORJSONResponse

class AppException(HTTPException):
    """
    Single reusable exception class for all errors.
    """
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
        source: str = "internal",
        details: dict | None = None,
    ):
        self.error_code = error_code
        self.source = source
        self.details = details or {}
        super().__init__(status_code=status_code, detail=message)


async def app_exception_handler(request: Request, exc: AppException):
    print("exc", exc)
    return ORJSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "state": (
                "clarification_required"
                if exc.error_code == "CLARIFICATION_REQUIRED"
                else "error"
            ),
            "status_code": exc.status_code,
            "message": exc.detail,
            "data": None,
            "error": {
                "code": exc.error_code,
                "source": exc.source,
                "details": exc.details
            },
            "meta": {
                "version": "1.0",
                "request_id": str(uuid.uuid4())
            }
        }
    )



async def generic_exception_handler(request: Request, exc: Exception):
    return ORJSONResponse(
        status_code=500,
        content={
            "success": False,
            "state": "error",
            "status_code": 500,
            "message": "Unexpected internal error.",
            "data": None,
            "error": {
                "code": "UNEXPECTED_ERROR",
                "source": "internal",
                "details": {}
            },
            "meta": {
                "version": "1.0",
                "request_id": str(uuid.uuid4())
            }
        }
    )