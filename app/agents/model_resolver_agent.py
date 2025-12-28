from app.core.llm import llm_client
from app.odoo.registry.registry_loader import load_odoo_registry


class ModelResolverAgent:
    def __init__(self):
        self.llm_client = llm_client

    def discover(self, user_input: str) -> list[str]:
        model_index = self._build_model_index()

        system_prompt = "You are an Odoo ERP model discovery engine. Always respond in valid JSON."
        user_prompt = f"""
                    User request: {user_input}
                    Available Odoo entities: {model_index}

                    Rules:
                    - Select all relevant models from the list.
                    - Output JSON only: {{ "models": [] }}.
                    - Do not add explanations.
                """

        response = self.llm_client.complete(system_prompt, user_prompt)
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

    def resolve_models(self, user_input: str) -> list[str]:
        mapping = {
            ("sale order line", "sale.order.line"),
            ("product category", "product.category"),
            ("product", "product.template"),
            ("customer", "res.partner"),
            ("invoice", "account.move"),
            ("order", "sale.order"),
            ("module", "ir.module.module"),
        }

        user_input = user_input.lower()
        matched = []

        for keyword, model in mapping:
            if keyword in user_input and model not in matched:
                matched.append(model)

        return matched
