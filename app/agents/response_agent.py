from app.responses import templates
from app.responses.polisher import polish_response
from app.exceptions.app_exceptions import AppException


class ResponseAgent:
    def respond(self, *, user_input: str, plan: dict, execution_log: list, clarification: dict | None = None) -> str:
        if clarification:
            return {
                "success": True,
                "status": "clarification_required",
                "status_code": 200,
                "message": "Additional information required",
                "data": {
                    "version": "1.0",
                    "summary": {
                        "text": clarification["summary_text"]
                    },
                    "blocks": [
                        {
                            "type": "info",
                            "data": {
                                "missing_fields": clarification["missing_fields"]
                            }
                        }
                    ]
                },
                "error": None,
                "meta": {
                    "needs_clarification": True
                }
            }

        if not execution_log:
            raise AppException(
                message="Execution failed. No steps were completed.",
                error_code="EXECUTION_FAILED",
                source="agent",
                status_code=500
            )

        return polish_response(user_input=user_input, plan=plan, result=execution_log)