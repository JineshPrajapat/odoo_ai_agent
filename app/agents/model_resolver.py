import difflib
from app.odoo.registry.registry_loader import load_odoo_registry

MODEL_ALIASES = {
    "customer": "res.partner",
    "client": "res.partner",
    "vendor": "res.partner",
    "supplier": "res.partner",
    "invoice": "account.move",
    "bill": "account.move",
    "sales order": "sale.order",
    "order": "sale.order",
    "product": "product.template",
}


class ModelResolver:
    def __init__(self):
        self.registry = load_odoo_registry()

    def resolve(self, text: str) -> list[str]:
        text = text.lower()
        models = set()

        # Tier 1: alias match
        for key, model in MODEL_ALIASES.items():
            if key in text and model in self.registry:
                models.add(model)

        # Tier 2: direct model name match
        for model in self.registry.keys():
            if model.replace(".", " ") in text:
                models.add(model)

        # Tier 3: fuzzy match on descriptions
        if not models:
            descriptions = {
                model: meta.get("description", "")
                for model, meta in self.registry.items()
            }

            matches = difflib.get_close_matches(
                text,
                descriptions.values(),
                n=3,
                cutoff=0.6
            )

            for model, desc in descriptions.items():
                if desc in matches:
                    models.add(model)

        return list(models)
