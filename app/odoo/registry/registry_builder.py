import json
from app.odoo.crud import OdooCRUD


OUTPUT_FILE = "app/odoo/registry/odoo_registry.json"

ALLOWED_MODELS = {
    "res.partner",
    "sale.order",
    "sale.order.line",
    "product.template",
    "account.move",
    "ir.module.module",
}


def build_registry():
    print("Authenticating with Odoo...")
    # uid = OdooAuthService.authenticate()
    client = OdooCRUD(2)

    registry = {}

    print("Fetching allowed models...")
    models = client.execute_kw(
        model="ir.model",
        method="search_read",
        args=[[("model", "in", list(ALLOWED_MODELS))]],
        kwargs={"fields": ["model", "name"]},
    )

    for model in models:
        model_name = model["model"]
        print(f"Processing model: {model_name}")

        # Fetch fields
        fields = client.execute_kw(
            model="ir.model.fields",
            method="search_read",
            args=[[("model", "=", model_name)]],
            kwargs={
                "fields": [
                    "name",
                    "ttype",
                    "required",
                    "relation",
                    "readonly",
                ]
            },
        )

        field_map = {}
        required_fields = []
        relational_fields = {}

        for field in fields:
            field_map[field["name"]] = {
                "type": field["ttype"],
                "readonly": field["readonly"],
            }

            if field["required"] and not field["readonly"]:
                required_fields.append(field["name"])

            if field["relation"]:
                relational_fields[field["name"]] = field["relation"]

        # Fetch access rights
        access = client.execute_kw(
            model="ir.model.access",
            method="search_read",
            args=[[("model_id.model", "=", model_name)]],
            kwargs={
                "fields": [
                    "perm_read",
                    "perm_create",
                    "perm_write",
                    "perm_unlink",
                ]
            },
        )

        permissions = {
            "read": any(a["perm_read"] for a in access),
            "create": any(a["perm_create"] for a in access),
            "update": any(a["perm_write"] for a in access),
            "delete": any(a["perm_unlink"] for a in access),
        }

        registry[model_name] = {
            "label": model["name"],
            "permissions": permissions,
            "required_fields_on_create": required_fields,
            "fields": field_map,
            "relations": relational_fields,
        }

    print(f"Writing registry to {OUTPUT_FILE}")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)

    print("Registry build complete.")


if __name__ == "__main__":
    build_registry()
