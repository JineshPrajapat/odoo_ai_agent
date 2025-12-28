from app.core.llm import llm_client
import json

PLANNER_SYSTEM_PROMPT = """
            You are an Odoo ERP action planner.
            - Always follow strict JSON schema.
            - Only use models and fields provided by the user.
            - Do NOT invent fields or models.
            - Each step must have a unique step_id.
            - Reference previous results using $step_id.field if needed.
            - If required data is missing, return action=clarify.
            - Return only valid JSON, no explanations, no extra text.
            - JSON must not have duplicate keys.

            PLANNING LOGIC:
            - If the user request can be fulfilled with the available information, return executable steps.
            - If required information is missing or ambiguous, DO NOT guess.
            - If you cannot safely build an executable plan, return exactly ONE step with:
                action = "clarify"

            CLARIFICATION STEP RULES:
            - action must be "clarify"
            - model must be null
            - domain, fields, ids must be empty
            - data must include:
                - summary_text: a clear, polite, human-readable question for the business user
                - missing_fields: list of required missing inputs

            JSON Output format example:
            {
                "steps": [
                    {
                    "step_id": "step_1",
                    "action": "read|search|create|update|delete|install_module|clarify",
                    "model": "<model or null>",
                    "domain": [],
                    "fields": [],
                    "data": {},
                    "ids": []
                    }
                ]
            }
        """


class PlannerAgent:
    def plan(self, *, user_input: str, registry_slice: dict) -> dict:
        """
        Generate a structured action plan using LLM.
        """
        system_prompt = "You are an Odoo ERP action planner. Strictly follow the JSON schema rules."
        user_prompt = self._build_prompt(user_input, registry_slice)
        plan = llm_client.complete(system_prompt=PLANNER_SYSTEM_PROMPT, user_prompt=user_prompt)

        return plan

    def _build_prompt(self, user_input: str, registry_slice: dict) -> str:
        return f"""
                Available Odoo models and fields (STRICT): {registry_slice}
                User request: {user_input}
            """

    def _parse_response(self, response: str) -> dict:
        # strict JSON parsing only
        return json.loads(response)
