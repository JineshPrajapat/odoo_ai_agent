def validate_plan(plan: dict, registry_slice: dict) -> dict:
    # 1. Validate plan structure
    steps = plan["steps"]
    if not steps or not isinstance(steps, list):
        return {
            "valid": False,
            "reason": "Plan must contain a list of steps"
        }
    
    # 2. Validate each step
    for step in steps:
        step_id = step.get("step_id", "unknown_step")
        model = step["model"]
        action = step["action"]

        if not model or not action:
            return {
                "valid": False,
                "step_id": step_id,
                "reason": "Each step must include model and action"
            }
        
        # 3. Validate model
        if model not in registry_slice:
            return {
                "needs_clarification": True,
                "step_id": step_id,
                "reason": f"Unknown model '{model}'"
            }
        
        allowed_actions = registry_slice[model].get("allowed_actions", [])
        # if action not in allowed_actions:
        #     return {
        #         "needs_clarification": True,
        #         "step_id": step_id,
        #         "reason": f"Action '{action}' not allowed for model '{model}'"
        #     }
        
        # 4. Action-specific validation
        if action == "create":
            required_fields = registry_slice[model].get(
                "required_fields_on_create", []
            )
            data = step.get("data", {})
            missing = [f for f in required_fields if f not in data]

            # if missing:
            #     return {
            #         "needs_clarification": True,
            #         "step_id": step_id,
            #         "missing_fields": missing
            #     }

        # if action in ("read", "update", "delete"):
        #     if not step.get("ids"):
        #         return {
        #             "needs_clarification": True,
        #             "step_id": step_id,
        #             "reason": f"'{action}' action requires record identifiers"
        #         }
            

    # 5. All steps valid
    return {"valid": True}