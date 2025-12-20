from app.odoo.request import OdooRequest
from app.core.config import ODOO_DB, ODOO_PASSWORD

class OdooModuleService:

    def __init__(self, uid: int):
        self.uid = uid
        self.client = OdooRequest()

    def install_module(self, module_name: str) -> bool:
        # Step 1: Search module
        module_ids = self.client.call(
            ODOO_DB,
            self.uid,
            ODOO_PASSWORD,
            "ir.module.module",
            "search",
            [[("name", "=", module_name)]],
        )

        if not module_ids:
            raise ValueError("Module not found")

        # Step 2: Install module
        self.client.call(
            ODOO_DB,
            self.uid,
            ODOO_PASSWORD,
            "ir.module.module",
            "button_immediate_install",
            [module_ids],
        )

        return True
