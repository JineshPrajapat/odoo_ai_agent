from app.core.llm import LLMClient

llm = LLMClient()

def polish_response(
    *,
    user_input: str,
    plan: dict,
    result: dict,
) -> str:
    prompt = f"""
                You are an AI assistant responding to a user after performing an operation in Odoo.

                User's original request:
                {user_input}

                Planned action (internal):
                {plan}

                Execution result:
                {result}

                Instructions:
                1 Respond in clear, friendly, professional English
                2 Do NOT mention technical terms (IDs, RPC, models, JSON)
                3 Confirm success or explain failure simply
                4 Assume the user is a business user
                5 Response format rules:
                    - Always provide a top-level JSON object with a "text" key containing a human-readable summary.
                    - If the result contains **lists or tables** of items (e.g., customers, products, orders):
                        - Include a "tables" key, which is a list of objects. Each object represents one table with:
                        {{
                            "title": "<table title>",
                            "columns": ["column1", "column2", ...],
                            "rows": [
                            ["value1", "value2", ...],
                            ...
                            ]
                        }}
                    - For simple single-record info, only include the "text" key.
                    - Always ensure the JSON is well-formed and parsable.

                5 Examples:
                    - Single record:
                        Request: "Show the last added customer"
                        Response:
                        {{
                            "text": "The last customer added is John Doe with email john@example.com."
                        }}

                    - Single table:
                        Request: "Show top 5 customers by purchases"
                        Response:
                        {{
                            "text": "Here are the top 5 customers with the highest purchases:",
                            "tables": [
                            {{
                                "title": "Top Customers",
                                "columns": ["Name", "Total Purchase"],
                                "rows": [
                                ["Customer A", "$5000"],
                                ["Customer B", "$4200"],
                                ["Customer C", "$3500"],
                                ["Customer D", "$3000"],
                                ["Customer E", "$2800"]
                                ]
                            }}
                            ]
                        }}

                    - Multiple tables:
                        Request: "List all customers and products added last month"
                        Response:
                        {{
                            "text": "Here are the customers and products added last month:",
                            "tables": [
                            {{
                                "title": "New Customers",
                                "columns": ["Name", "Email", "City"],
                                "rows": [
                                ["Customer X", "x@example.com", "New York"],
                                ["Customer Y", "y@example.com", "London"]
                                ]
                            }},
                            {{
                                "title": "New Products",
                                "columns": ["Name", "Category", "Price"],
                                "rows": [
                                ["Product A", "Category 1", "$100"],
                                ["Product B", "Category 2", "$150"]
                                ]
                            }}
                            ]
                        }}

                    - If no data found:
                        Request: "List customers with purchases over $100000 last month"
                        Response:
                        {{
                            "text": "No customers were found with purchases over $100,000 last month."
                        }}

                Final response:
            """
    return llm.generate(prompt)
