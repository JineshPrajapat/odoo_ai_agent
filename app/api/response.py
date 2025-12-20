from typing import Any, Optional

import json
from typing import Any

def success_response(
    *,
    data: Any = None,
    message: str = "Success",
    status_code: int = 200,
) -> dict:
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            data = {"text": data}
    elif data is None:
        data = {}

    return {
        "status": "success",
        "status_code": status_code,
        "message": message,
        "data": data,
    }



def error_response(
    *,
    message: str,
    status_code: int = 400,
    error_code: Optional[str] = None,
) -> dict:
    return {
        "status": "error",
        "status_code": status_code,
        "message": message,
        "error_code": error_code,
    }
