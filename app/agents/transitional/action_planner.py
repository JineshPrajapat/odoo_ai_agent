ACTION_TO_ODOO_METHOD = {
    "read": "search_read",
    "create": "create",
    "update": "write",
    "delete": "unlink",
    "search": "search",
    "install_module": "button_immediate_install",
}

def plan_action(user_input: str, registry_slice: dict) -> dict:
    text = user_input.lower()

    for model, meta in registry_slice.items():
        allowed_actions = meta.get("allowed_actions", [])
        print("allowed_actions:", allowed_actions)

        # CREATE
        if "create" in text and "create" in allowed_actions:
            return {
                "model": model,
                "action": "create",
                "method": ACTION_TO_ODOO_METHOD["create"],
            }

        # UPDATE
        if any(x in text for x in ["update", "modify", "change"]) and "update" in allowed_actions:
            return {
                "model": model,
                "action": "update",
                "method": ACTION_TO_ODOO_METHOD["update"],
            }

        # DELETE
        if any(x in text for x in ["delete", "remove"]) and "delete" in allowed_actions:
            return {
                "model": model,
                "action": "delete",
                "method": ACTION_TO_ODOO_METHOD["delete"],
            }

        # READ
        if any(x in text for x in ["get", "list", "show", "fetch"]) and "read" in allowed_actions:
            return {
                "model": model,
                "action": "read",
                "method": ACTION_TO_ODOO_METHOD["read"],
            }

    return {"needs_clarification": True}
