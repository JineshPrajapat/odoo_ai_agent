def validate_plan(plan: dict, registry_slice: dict) -> dict:
    model = plan["model"]
    action = plan["action"]

    if model not in registry_slice:
        return {"needs_clarification": True, "reason": "Unknown model"}

    if action not in registry_slice[model]["allowed_actions"]:
        return {"needs_clarification": True, "reason": "Action not allowed"}

    if action == "create":
        missing = [
            f for f in registry_slice[model]["required_fields_on_create"]
            if f not in plan.get("data", {})
        ]
        if missing:
            return {"needs_clarification": True, "missing_fields": missing}

    # if plan.get("confidence", 0) < 0.6:
    #     return {"needs_clarification": True, "reason": "Low confidence"}

    return {"valid": True}
