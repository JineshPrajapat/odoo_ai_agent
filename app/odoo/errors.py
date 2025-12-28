class OdooExecutionError(Exception):
    def __init__(self, message: str, source="odoo"):
        self.message = message
        self.source = source
        super().__init__(message)

    
    def _handle_odoo_error(self, error: RuntimeError, plan: dict) -> dict:
        raw = error.args[0] if error.args else {}

        return {
            "success": False,
            "error": {
                "type": "ODOO_VALIDATION_ERROR",
                "model": plan.get("model"),
                "action": plan.get("action"),
                "message": raw.get("data", {}).get("message", "Odoo operation failed"),
                "debug": raw.get("data", {}).get("debug")
            }
        }
