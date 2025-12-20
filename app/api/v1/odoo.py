from fastapi import APIRouter, HTTPException
from app.schemas.odoo import OdooExecuteRequest, OdooModuleInstallPayload
from app.odoo.service import OdooService
from app.odoo.auth import OdooAuthService

router = APIRouter(prefix="/odoo", tags=["Odoo"])

@router.post("/execute")
def execute_odoo_action(payload: OdooExecuteRequest):
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

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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