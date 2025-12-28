from app.odoo.crud import OdooCRUD
from app.odoo.errors import OdooExecutionError

class OdooService:
    def __init__(self, uid: int):
        self.crud = OdooCRUD(uid)

    def execute_safe(self, step: dict) -> dict:
        try:
            result = self.execute(step)
            return {
                "success": True,
                "data": result.get("data"),
                "error": None
            }
        
        except OdooExecutionError as e:
            print("odoo execution error", e)
            return {
                "success": False,
                "data": None,
                "error": {
                    "type": "ODOO_ERROR",
                    "message": e.message,
                    "source": e.source,
                    "details": e.details,
                }
            }

        except ValueError as e:
            return {
                "success": False,
                "data": None,
                "error": {
                    "type": "VALIDATION_ERROR",
                    "message": str(e),
                    "source": "agent",
                }
            }
    
        except Exception as e:
            print("exceptipo oddo", e)
            return {
                "success": False,
                "data": None,
                "error": {
                    "type": "INTERNAL_ERROR",
                    "message": str(e),
                    "source": "internal",
                    "details": {"exception": str(e)},
                }
            }

    def execute(self, plan: dict):
        action = plan["action"]

        # Non-CRUD actions FIRST
        if action == "install_module" or action == "install":
            module_name = plan["module_name"]
            if not module_name:
                raise ValueError("module_name is required for install_module")
            return {
                "message": f"Module '{module_name}' installed successfully",
                "data": self.install_module(module_name)
            }

        model = plan["model"]

        if not model:
            raise ValueError(f"Model is required for action '{action}'")

        if action == "search" or action == "search_read":
            fields = plan.get("fields")
            if fields:
                records = self.crud.read(
                    model=model, domain=plan.get("domain"), fields=fields)
                return {"message": f"Found {len(records)} records in {model}", "data": records}
            else:
                # Only return IDs if no fields specified
                record_ids = self.crud.search(
                    model=model, domain=plan.get("domain"))
                return {"message": f"Found {len(record_ids)} records in {model}", "data": record_ids}

        if action == "create":
            return {"data": {"id": self.crud.create(model, plan["data"])}}

        if action == "update":
            ids = plan.get("ids", [])
            if not ids:
                raise ValueError("IDs are required for update")
            self.crud.update(
                model=model,
                ids=plan.get("ids"),
                values=plan.get("data")
            )
            return {"data": {"id": self.crud.create(model, plan["data"])}}

        if action == "delete":
            ids = plan.get("ids", [])
            if not ids:
                raise ValueError("IDs are required for delete")
            self.crud.delete(
                model=model,
                ids=plan.get("ids")
            )
            return {"data": {"deleted": True}}

        raise ValueError(f"Unsupported action: {action}")

    def install_module(self, module_name: str):
        module_ids = self.crud.search(
            model="ir.module.module",
            domain=[("name", "=", module_name)],
            # fields=["id", "state"]
        )

        print("module_ids", module_ids)

        if not module_ids:
            raise ValueError("Module not found")

        self.crud.update(
            model="ir.module.module",
            ids=module_ids,
            values={"state": "uninstalled"}
        )

        self.crud.execute_kw(
            model="ir.module.module",
            method="button_immediate_install",
            args=[module_ids]
        )

        return module_ids

    def list_installed_modules(self):
        """
        Returns a list of all installed modules with their name and state.
        """
        modules = self.crud.read(
            model="ir.module.module",
            domain=[("state", "=", "installed")],
            fields=["id", "name", "shortdesc", "state"]
        )

        if not modules:
            return {"success": False, "message": "No modules are currently installed."}

        return {"success": True, "modules": modules}
