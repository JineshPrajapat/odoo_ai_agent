from sqlalchemy import Column, String, ForeignKey, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from sqlalchemy.sql import func
import uuid

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    cs_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    u_id = Column(UUID(as_uuid=True), ForeignKey("users.u_id", ondelete="CASCADE"), nullable=False)
    title = Column(Text)
    # odoo_connection_id = Column(
    #     UUID(as_uuid=True),
    #     ForeignKey("odoo_connections.id", ondelete="SET NULL"),
    #     nullable=True
    # )

    status = Column(String(50), default="active")  # active / completed / failed

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
