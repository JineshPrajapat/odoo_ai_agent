import requests
from app.core.config import ODOO_URL, ODOO_DB, ODOO_PASSWORD
import uuid


class OdooRequest:
    def __init__(self):
        self.url = f"{ODOO_URL}/jsonrpc"

    def _raw_call(self, payload: dict):
        r = requests.post(self.url, json=payload, timeout=15)
        r.raise_for_status()

        response = r.json()
        if "error" in response:
            raise RuntimeError(response["error"])

        return response.get("result")

    def call(self, db, uid, password, model, method, args=None, kwargs=None):
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    db,
                    uid,
                    password,
                    model,
                    method,
                    args or [],
                    kwargs or {},
                ],
            },
            "id": str(uuid.uuid4()),
        }

        return self._raw_call(payload)
    
