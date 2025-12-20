from app.agents.model_resolver import ModelResolver
from app.odoo.registry.registry_slice import build_llm_registry_slice
from app.agents.transitional.action_planner import plan_action
from app.agents.transitional.clarifier import generate_clarification

class AgentOrchestrator:
    def __init__(self):
        self.resolver = ModelResolver()

    def run(self, text: str) -> dict:
        models = self.resolver.resolve(text)
        print("resolved model: ", models)

        if not models:
            return {
                "needs_clarification": True,
                "message": "Could not determine the target Odoo model."
            }

        sliced = build_llm_registry_slice(models=models)
        plan = plan_action(text, sliced)
        print("planned action", plan)

        if plan.get("needs_clarification"):
            return {
                "needs_clarification": True,
                "message": generate_clarification(sliced)
            }

        return {
            "ready": True,
            "plan": plan
        }
