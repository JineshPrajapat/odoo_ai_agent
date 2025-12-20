from app.odoo.registry.registry_loader import load_odoo_registry


def build_llm_registry_slice(
    *,
    models: list[str],
    include_relations: bool = True,
) -> dict:
    """
    Build a minimal, LLM-safe registry slice.
    """
    full_registry = load_odoo_registry()
    slice_registry = {}

    for model in models:
        meta = full_registry.get(model)
        if not meta:
            continue

        allowed_actions = [
            action
            for action, allowed in meta["permissions"].items()
            if allowed
        ]

        slice_registry[model] = {
            "label": meta.get("label"),
            "allowed_actions": allowed_actions,
            "required_fields_on_create": meta.get(
                "required_fields_on_create", []
            ),
            "fields": _compress_fields(meta.get("fields", {})),
        }

        if include_relations:
            slice_registry[model]["relations"] = meta.get(
                "relations", {}
            )

    return slice_registry


def _compress_fields(fields: dict) -> dict:
    """
    Reduce field metadata for LLM consumption.
    """
    compressed = {}
    for name, info in fields.items():
        if info.get("readonly"):
            continue
        compressed[name] = info["type"]
    return compressed
