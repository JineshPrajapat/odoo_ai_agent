from app.core.config import ODOO_DB, ODOO_USER, ODOO_PASSWORD
from app.odoo.request import OdooRequest

class OdooAuthService:
    def __init__(self):
        self.client = OdooRequest()

    def authenticate(self) -> int:
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "common",
                "method": "authenticate",
                "args": [
                    ODOO_DB,
                    ODOO_USER,
                    ODOO_PASSWORD,
                    {},
                ],
            },
            "id": "auth",
        }

        result = self.client._raw_call(payload)

        if not result:
            raise RuntimeError("Odoo authentication failed")

        return result
