import json
from pathlib import Path

REGISTRY_PATH = Path("app/odoo/registry/odoo_registry.json")
_REGISTRY = None

def load_odoo_registry() -> dict:
    global _REGISTRY
    if _REGISTRY is None:
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            _REGISTRY = json.load(f)
    return _REGISTRY
