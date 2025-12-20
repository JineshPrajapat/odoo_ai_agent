# schemas/chat.py
from pydantic import BaseModel

class ChatRequest(BaseModel):
    # session_id: str
    message: str

class ChatResponse(BaseModel):
    message: str
    data: dict | None = None
    requires_confirmation: bool = False
