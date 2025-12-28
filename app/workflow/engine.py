from app.agents.model_resolver import ModelResolver
from app.agents.planner_agent import PlannerAgent
from app.workflow.validator import validate_plan
from app.workflow.clarification import generate_clarification
from app.odoo.registry.registry_slice import build_llm_registry_slice
from app.odoo.service import OdooService
from app.agents.response_agent import ResponseAgent
from app.agents.model_resolver_agent import ModelResolverAgent
from app.exceptions.error_factory import (
    raise_clarification_required,
    raise_validation_error
)

class ExecutionContext:
    def __init__(self):
        self.step_results = {}
        self.variables = {}
        self.execution_log = []

class WorkflowEngine:
    def run(self, *, user_input: str, odoo_uid: int):
        # models = ModelResolver().resolve(user_input)
        models = ModelResolverAgent().resolve_models(user_input=user_input)
        # models = ModelResolverAgent().discover(user_input=user_input)
        print("resolved model", models)

        if not models:
            raise_clarification_required(
                "Which Odoo entity are you referring to?",
                {"missing_fields": ["model"]}
            )

        registry_slice = build_llm_registry_slice(models=models, include_relations=True)
        print("registry_slice", registry_slice)

        plan = PlannerAgent().plan(
            user_input=user_input,
            registry_slice=registry_slice
        )
        print(f"Planned action: {plan}")

        first_step = plan["steps"][0]

        if first_step["action"] == "clarify":
            return ResponseAgent().respond(
                user_input=user_input,
                plan=plan,
                execution_log=[],
                clarification=first_step["data"]
            )

        validation = validate_plan(plan, registry_slice)
        if validation.get("needs_clarification"):
            raise_validation_error(
                "More information required.",
                validation
            )

        print("validation", validation)

        context = ExecutionContext()
        odooService = OdooService(uid=odoo_uid)
        for step in plan["steps"]:
            print("Steps:", step)
            self._execute_step(step, odooService, context=context)

        print("context.execution_log", context.execution_log)
        return ResponseAgent().respond(
            user_input=user_input,
            plan=plan,
            execution_log=context.execution_log
        )

    def _execute_step(self, step: dict, odoo_service: OdooService, context: ExecutionContext):
        resolved_step = self._resolve_dependencies(step, context.variables)
        result = odoo_service.execute_safe(resolved_step)

        self._store_result(step["step_id"], result, context)
        self._log_step(step, result, context)

        if not result.get("success"):
            raise StopIteration

    def _resolve_dependencies(self, step: dict, variables: dict):
        def resolve(value):
            if isinstance(value, str) and value.startswith("$"):
                return variables.get(value[1:])
            if isinstance(value, dict):
                return {k: resolve(v) for k, v in value.items()}
            if isinstance(value, list):
                return [resolve(v) for v in value]
            return value

        return resolve(step)

    def _store_result(self, step_id: str, result: dict, context: ExecutionContext):
        context.step_results[step_id] = result

        if not result.get("success"):
            return

        data = result.get("data", {})
        if isinstance(data, dict):
            for key, value in data.items():
                context.variables[f"{step_id}.{key}"] = value

    def _log_step(self, step: dict, result: dict, context: ExecutionContext):
        context.execution_log.append({
            "step_id": step["step_id"],
            "action": step["action"],
            "model": step.get("model"),
            "success": result.get("success", False),
            "data": result.get("data"),
            "error": result.get("error")
        })
