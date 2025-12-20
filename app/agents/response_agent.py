from app.responses import templates
from app.responses.polisher import polish_response

class ResponseAgent:
    def respond(
        self,
        *,
        user_input: str,
        plan: dict,
        execution_result: dict,
    ) -> str:

        action = plan["action"]

        # --- Deterministic paths (NO LLM) ---
        if action == "create":
            return templates.create_template()

        if action == "update":
            return templates.update_template()

        if action == "delete":
            return templates.delete_template()

        # --- Hybrid paths (LLM-polished) ---
        if action in ("read", "install"):
            return polish_response(
                user_input=user_input,
                plan=plan,
                result=execution_result,
            )

        # --- Fallback ---
        return "The operation was completed."
