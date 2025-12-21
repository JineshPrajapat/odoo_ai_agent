# from app.odoo.request import OdooRequest

# class OdooService:
#     def execute(self, plan):
#         client = OdooRequest()

#         if plan["action"] == "read":
#             data = client.search_read(plan["model"])
#             return {"message": "Here are the results", "data": data}

#         if plan["action"] == "create":
#             record_id = client.create(plan["model"], plan["data"])
#             return {"message": "Record created", "data": {"id": record_id}}

        

from app.odoo.crud import OdooCRUD

class OdooService:
    def __init__(self, uid: int):
        self.crud = OdooCRUD(uid)

    def execute(self, plan: dict):
        action = plan["action"]

        # Non-CRUD actions FIRST
        if action == "install_module":
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

        if action == "read":
            data = self.crud.read(
                model=model,
                domain=plan.get("domain"),
                fields=plan.get("fields"),
            )
            return {"message": "Here are the results", "data": data}

        if action == "create":
            record_id = self.crud.create(
                model=model,
                values=plan["data"]
            )
            return {"message": "Record created", "data": {"id": record_id}}
        
        if action == "update":
            self.crud.update(
                model=model,
                ids=plan.get("ids"),
                values=plan.get("data")
            )
            return {"message": "Record updated"}

        if action == "delete":
            self.crud.delete(
                model=model,
                ids=plan.get("ids")
            )
            return {"message": "Record deleted"}
        
        if action == "search":
            self.crud.search(
                model=model,
                domain=plan.get("domain"),
                limit=plan.get("limit", 0),
                order=plan.get("order", "")
            )

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