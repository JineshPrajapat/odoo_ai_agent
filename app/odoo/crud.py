from app.odoo.request import OdooRequest
from app.core.config import ODOO_DB, ODOO_PASSWORD

class OdooCRUD:

    def __init__(self, uid: int):
        self.uid = uid
        self.client = OdooRequest()

    def create(self, model: str, values: dict) -> int:
        return self.client.call(
            ODOO_DB,
            self.uid,
            ODOO_PASSWORD,
            model,
            "create",
            [values],
        )

    def read(self, model: str, domain: list, fields: list):
        return self.client.call(
            ODOO_DB,
            self.uid,
            ODOO_PASSWORD,
            model,
            "search_read",
            [domain],
            {"fields": fields},
        )

    def update(self, model: str, ids: list, values: dict) -> bool:
        return self.client.call(
            ODOO_DB,
            self.uid,
            ODOO_PASSWORD,
            model,
            "write",
            [ids, values],
        )

    def delete(self, model: str, ids: list) -> bool:
        return self.client.call(
            ODOO_DB,
            self.uid,
            ODOO_PASSWORD,
            model,
            "unlink",
            [ids],
        )
    
    def search(self, model: str, domain: list, limit: int = 0, order: str = "") -> list[int]:
        """
        Search for record IDs in the given model using the domain filter.
        :param model: Odoo model name
        :param domain: List of domain filters, e.g., [('name', '=', 'sale')]
        :param limit: Max number of records to return (0 = all)
        :param order: Ordering string, e.g., 'name asc'
        :return: List of record IDs
        """
        return self.client.call(
            ODOO_DB,
            self.uid,
            ODOO_PASSWORD,
            model,
            "search",
            [domain],
            {"limit": limit, "order": order},
        )
    
    def execute_kw(self, model, method, args=None, kwargs=None):
        return self.client.call(
            ODOO_DB,
            self.uid,
            ODOO_PASSWORD,
            model=model,
            method=method,
            args=args,
            kwargs=kwargs,
        )