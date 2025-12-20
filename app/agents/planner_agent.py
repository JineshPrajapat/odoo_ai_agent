from app.core.llm import llm_client
import json

class PlannerAgent:
    def plan(self, *, user_input: str, registry_slice: dict) -> dict:
        """
        Generate a structured action plan using LLM.
        """

        prompt = self._build_prompt(user_input, registry_slice)
        response = llm_client.complete(prompt)

        print("LLM response", response)

        plan = response
        return plan

    def _build_prompt(self, user_input: str, registry_slice: dict) -> str:
        return f"""
                You are an Odoo ERP action planner.

                User request:
                {user_input}

                Available Odoo models and fields (STRICT):
                {registry_slice}

                Rules:
                - You MUST select a model from the registry
                - You MUST use ONLY fields present in the registry
                - Do NOT invent fields or models
                - Choose ONE action only:
                read | create | update | delete | install_module | clarify
                - If required data is missing, return action=clarify
                - Output MUST be valid JSON only
                - Do NOT include explanations

                JSON formats:

                READ:
                {{
                "action": "read",
                "model": "<model>",
                "domain": [],
                "fields": []
                }}

                CREATE:
                {{
                "action": "create",
                "model": "<model>",
                "data": {{}}
                }}

                UPDATE:
                {{
                "action": "update",
                "model": "<model>",
                "ids": [],
                "data": {{}}
                }}

                DELETE:
                {{
                "action": "delete",
                "model": "<model>",
                "ids": []
                }}

                INSTALL MODULE:
                {{
                "action": "install_module",
                "module_name": "<technical_name>"
                }}

                CLARIFY:
                {{
                "action": "clarify",
                "message": "<question>"
                }}
            """

    def _parse_response(self, response: str) -> dict:
        # strict JSON parsing only
        return json.loads(response)
