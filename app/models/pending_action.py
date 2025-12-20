from sqlalchemy import Column, String, JSON, ForeignKey, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from sqlalchemy.sql import func
import uuid

class PendingAction(Base):
    __tablename__ = "pending_actions"

    pa_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cs_id = Column(
        UUID(as_uuid=True),
        ForeignKey("chat_sessions.cs_id", ondelete="CASCADE"),
        nullable=False
    )

    action_type = Column(String(100), nullable=False)
    payload = Column(JSON, nullable=False)

    # odoo_model = Column(String(255))
    # odoo_method = Column(String(255))
    
    status = Column(String(50), default="pending")
    error_message = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
