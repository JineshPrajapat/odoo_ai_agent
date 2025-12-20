from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.transitional.orchestrator import AgentOrchestrator

router = APIRouter()
agent = AgentOrchestrator()

class AgentInput(BaseModel):
    text: str

router = APIRouter(prefix="/agent_test", tags=["Testing agent"])

@router.post("/test")
def test_agent(payload: AgentInput):
    return agent.run(payload.text)
