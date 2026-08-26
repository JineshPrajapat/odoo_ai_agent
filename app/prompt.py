user_input= ""
plan_str=""
result_str=""

prompt = f"""
                User request: {user_input}
                Planned action (internal): {plan_str}
                Execution result: {result_str}

                Task: Summarize the outcome clearly for a non-technical user. 

                Instructions:
                1 Return a single top-level JSON object.
                2 Include "text" with a friendly summary.
                3 Confirm success or explain failure simply
                4 Use "blocks" only if structured data exists; otherwise, keep blocks empty
                6 If no records, set meta.empty = true and blocks = []
                
                JSON output format:
                    {{
                        "version": "1.0",
                        "summary": {{
                            "text": "<human-readable message>"
                        }},
                        "blocks": [],
                        "meta": {{
                            "status": "success | warning | error",
                            "empty": false
                        }}
                    }}

                    Blocks rules:
                    - Use "blocks" only when structured data is present
                    - table: columns + rows  
                    - list: items  
                    - record: key-value fields  
                    - chart: chartType + labels + values 
                    - Multiple blocks are allowed

                    Block schemas:

                    Table:
                    {{
                        "type": "table",
                        "title": "<optional>",
                        "data": {{
                            "columns": ["<string>"],
                            "rows": [["<value>"]]
                        }}
                    }}

                    List:
                    {{
                        "type": "list",
                        "title": "<optional>",
                        "data": {{
                            "items": ["<string>"]
                        }}
                    }}

                    Record:
                    {{
                        "type": "record",
                        "title": "<optional>",
                        "data": {{
                            "<label>": "<value>"
                        }}
                    }}

                    Chart:
                    {{
                        "type": "chart",
                        "title": "<optional>",
                        "data": {{
                            "chartType": "bar | line | pie",
                            "labels": ["<string>"],
                            "values": ["<value>"]
                        }}
                    }}

                    Generate the final response JSON now.
            """



registry_slice=""
planner_prompt= f"""
                Available Odoo models and fields (STRICT): {registry_slice}
                User request: {user_input}

                Rules:
                - You may return ONE or MULTIPLE steps
                - Each step must have a unique id
                - Steps may reference previous results using $step_id.field
                - Use ONLY provided models and fields
                - Do NOT invent fields or models
                - If required data is missing, return action=clarify
                - Do NOT include explanations
                - Return ONLY a valid JSON object. Do NOT include any text outside JSON.
                - JSON must have no duplicate keys.

                JSON formats:
                {{
                "steps": [
                    {{
                    "step_id": "step_1",
                    "action": "read|search|create|update|delete|install_module|clarify",
                    "model": "<model>",
                    "domain": [],
                    "fields": [],
                    "data": {{}},
                    "ids": []
                    }}
                ]
                }}
            """