import json
from openai import OpenAI
from app.core.config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

class LLMClient:
    def complete(self, prompt: str) -> dict:
        try:
            response = client.chat.completions.create(
                model= OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a precise ERP planning engine."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0,
            )

            content = response.choices[0].message.content.strip()

            return json.loads(content)

        except json.JSONDecodeError:
            raise ValueError(f"LLM returned invalid JSON:\n{content}")

        except Exception as e:
            raise ValueError(f"LLM request failed: {str(e)}")


    def generate(self, prompt: str) -> str:
        ''' Generate a text response '''
        try:
            response = client.chat.completions.create(
                model= OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise ValueError(f"LLM generate failed: {str(e)}")

llm_client = LLMClient()
