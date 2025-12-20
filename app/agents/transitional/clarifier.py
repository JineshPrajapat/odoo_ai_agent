def generate_clarification(registry_slice: dict) -> str:
    if not registry_slice:
        return "Which Odoo entity are you referring to? For example: customer, invoice, product."

    model = next(iter(registry_slice.keys()))
    fields = registry_slice[model].get("fields", {})

    required = [
        name for name, meta in fields.items()
        if meta.get("required")
    ]

    if required:
        return f"Please provide values for: {', '.join(required)}"

    return "Please clarify the action you want to perform."
