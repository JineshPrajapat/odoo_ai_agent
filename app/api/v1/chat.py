from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.chat import ChatRequest
from app.api.response import success_response, error_response
from app.workflow.engine import WorkflowEngine
from app.core.database import get_db
from app.odoo.auth import OdooAuthService

router = APIRouter(prefix="/chat", tags=["agent"])

@router.post("/agent")
def test_agent(
    payload: ChatRequest,
    db: Session = Depends(get_db),
):
    """
    Test endpoint for AI → Odoo execution.
    """

    try:
        uid = OdooAuthService().authenticate()

        ODOO_UID = uid

        response = WorkflowEngine().run(
            user_input=payload.message,
            odoo_uid=ODOO_UID,
        )

        return success_response(
            data=response,
            message="Request processed successfully",
        )

    except ValueError as e:
        return error_response(
            message=str(e),
            status_code=400,
            error_code="VALIDATION_ERROR",
        )

    except TimeoutError:
        return error_response(
            message="Operation timed out. Please try again.",
            status_code=504,
            error_code="TIMEOUT",
        )

    except Exception:
        # DO NOT leak internal errors
        return error_response(
            message="Something went wrong while processing your request.",
            status_code=500,
            error_code="INTERNAL_ERROR",
        )

# @router.get("/secure")
# def secure_endpoint(request: Request):
#     user_id = getattr(request.state, "user_id", None)
#     if not user_id:
#         raise HTTPException(status_code=401, detail="Unauthorized")

#     return {"message": "Access granted", "user_id": user_id}  