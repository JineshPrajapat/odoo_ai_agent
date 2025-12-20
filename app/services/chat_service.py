from app.workflow.engine import WorkflowEngine
from app.agents.response_agent import ResponseAgent

class ChatService:
    def handle(self, payload):
        return WorkflowEngine().run(payload.message, payload.session_id)