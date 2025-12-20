from app.agents.model_resolver import ModelResolver
from app.agents.planner_agent import PlannerAgent
from app.workflow.validator import validate_plan
from app.workflow.clarification import generate_clarification
from app.odoo.registry.registry_slice import build_llm_registry_slice
from app.odoo.service import OdooService
from app.agents.response_agent import ResponseAgent

class WorkflowEngine:
    def run(self, *, user_input: str, odoo_uid: int):
        try:
            models = ModelResolver().resolve(user_input)

            if not models:
                return generate_clarification("Which Odoo entity are you referring to?")

            registry_slice = build_llm_registry_slice(models=models)

            plan = PlannerAgent().plan(
                user_input=user_input,
                registry_slice=registry_slice
            )
            print(f"Planned action: {plan}")

            validation = validate_plan(plan, registry_slice)
            if validation.get("needs_clarification"):
                return generate_clarification(validation)

            execution_result = OdooService(uid=odoo_uid).execute(plan)
            print(f"Execution result: {execution_result}")

            return ResponseAgent().respond(
                user_input=user_input,
                plan=plan,
                execution_result=execution_result,
            )

        except ValueError as ve:
            print(f"ValueError: {ve}")
            return {"status": "error", "message": str(ve)}

        except TimeoutError as te:
            print(f"TimeoutError: {te}")
            return {"status": "error", "message": "Operation timed out. Please try again."}

        except Exception as e:
            print("Unexpected error in WorkflowEngine",e)
            return {"status": "error", "message": "Something went wrong while processing your request."}
