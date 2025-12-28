from fastapi import APIRouter, HTTPException
from app.schemas.odoo import OdooExecuteRequest, OdooModuleInstallPayload
from app.odoo.service import OdooService
from app.odoo.auth import OdooAuthService
from app.odoo.errors import OdooExecutionError
router = APIRouter(prefix="/odoo", tags=["Odoo"])

@router.post("/execute")
def execute_odoo_action(payload: OdooExecuteRequest | OdooModuleInstallPayload):
    try:
        # Step 1: Authenticate to Odoo and get uid
        uid = OdooAuthService().authenticate()

        # Step 2: Execute dynamic Odoo plan
        service = OdooService(uid)
        result = service.execute(payload.dict(exclude_none=True))

        return {
            "success": True,
            "result": result,
        }

    except OdooExecutionError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "success": False,
                "error": e.to_dict(),
            },
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "error": {
                    "type": "VALIDATION_ERROR",
                    "message": str(e),
                    "source": "api",
                },
            },
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "type": "INTERNAL_ERROR",
                    "message": "Unexpected server error",
                    "source": "api",
                },
            },
        )


@router.post("/modules/install")
def install_odoo_module(
    payload: OdooModuleInstallPayload,
):
    try:
        uid = OdooAuthService().authenticate()

        # Step 2: Execute dynamic Odoo plan
        service = OdooService(uid)
        result = service.install_module(payload.module_name)

        if result == True :
            return {
                "success": True,
                "message": f"Module '{payload.module_name}' installation started"
            }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))