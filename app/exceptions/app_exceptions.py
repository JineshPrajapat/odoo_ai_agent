from fastapi import HTTPException, Request
from fastapi.responses import ORJSONResponse
# from loguru import logger

class AppException(HTTPException):
    """
    Single reusable exception class for all errors.
    """
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
        source: str = "internal"
    ):
        self.error_code = error_code
        self.source = source
        super().__init__(status_code=status_code, detail=message)


async def app_exception_handler(request: Request, exc: AppException):
    """
    Global handler for AppException
    """
    # logger.error(f"[{exc.source}] {exc.error_code} - {exc.detail}")
    return ORJSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.error_code,
            "source": exc.source,
            "message": exc.detail
        },
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """
    Catch-all handler for unexpected errors
    """
    # logger.exception(exc)
    return ORJSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "UNEXPECTED_ERROR",
            "source": "internal",
            "message": str(exc)
        },
    )
