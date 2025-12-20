from sqlalchemy import Column, String, ForeignKey, Text, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from sqlalchemy.sql import func
import uuid

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    cm_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cs_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.cs_id", ondelete="CASCADE"), nullable=False)
    sender = Column(String(20), nullable=False) # user / assistant /system
    message = Column(Text, nullable=False)
    metadata = Column(JSON)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
