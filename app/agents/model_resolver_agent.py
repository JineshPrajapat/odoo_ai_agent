from app.core.llm import llm_client
from app.odoo.registry.registry_loader import load_odoo_registry


class ModelResolverAgent:
    def __init__(self):
        self.llm_client = llm_client

    def discover(self, user_input: str) -> list[str]:
        model_index = self._build_model_index()

        prompt = f"""
                    You are an Odoo ERP model discovery engine.

                    User request:
                    {user_input}

                    Available Odoo entities:
                    {model_index}

                    Rules:
                    - Select ALL relevant models
                    - Use only models from the list
                    - Output JSON only
                    - No explanations

                    JSON format:
                    {{ "models": [] }}
                """

        response = self.llm_client.complete(prompt)
        models = response.get("models", [])

        return models

    def _build_model_index(self) -> dict:
        """
        Minimal semantic index for model discovery.
        """
        registry = load_odoo_registry()
        index = {}

        for model, meta in registry.items():
            index[model] = {
                "label": meta.get("label"),
            }

        return index
