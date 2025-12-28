from app.exceptions.app_exceptions import AppException

def raise_validation_error(message, details=None):
    raise AppException(
        message=message,
        error_code="VALIDATION_ERROR",
        status_code=400,
        source="agent",
        details=details
    )


def raise_clarification_required(message, details):
    raise AppException(
        message=message,
        error_code="CLARIFICATION_REQUIRED",
        status_code=200,
        source="agent",
        details=details
    )


def raise_llm_error(message):
    raise AppException(
        message=message,
        error_code="LLM_ERROR",
        status_code=502,
        source="llm"
    )


def raise_timeout():
    raise AppException(
        message="Operation timed out. Please try again.",
        error_code="TIMEOUT",
        status_code=504,
        source="system"
    )
