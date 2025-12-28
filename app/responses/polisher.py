from app.core.llm import LLMClient
import json

llm = LLMClient()

def polish_response(
    *,
    user_input: str,
    plan: dict,
    result: list,
) -> str:
    plan_str = json.dumps(plan, indent=2)
    result_str = json.dumps(result, indent=2)

    RESPONSE_FORMAT_SYSTEM_PROMPT = """
                You are an AI assistant preparing a final JSON response for a business user.
                Always return STRICT JSON only.
                Do NOT include Markdown, explanations, or technical terms.

                Permanent JSON output rules:
                - Return a single top-level object.
                - Include "text" with a human-readable summary.
                - Include "blocks" only if structured data exists; otherwise, blocks = []
                - meta.status = "success | warning | error"
                - meta.empty = true if no records
                - JSON must be valid and follow schema:

                {
                "version": "1.0",
                "summary": {"text": "<human-readable message>"},
                "blocks": [],
                "meta": {"status": "success|warning|error", "empty": false}
                }

                Block rules:
                - table: {"type":"table","title":"<optional>","data":{"columns":["<string>"],"rows":[["<value>"]]}}
                - list: {"type":"list","title":"<optional>","data":{"items":["<string>"]}}
                - record: {"type":"record","title":"<optional>","data":{"<label>":"<value>"}}
                - chart: {"type":"chart","title":"<optional>","data":{"chartType":"bar|line|pie","labels":["<string>"],"values":["<value>"]}}
            """
    
    prompt = f"""
                User request: {user_input}
                Planned action (internal): {plan_str}
                Execution result: {result_str}

                Task: Summarize the outcome clearly for a non-technical user. 
            """
    return llm.complete(system_prompt=RESPONSE_FORMAT_SYSTEM_PROMPT, user_prompt=prompt)
