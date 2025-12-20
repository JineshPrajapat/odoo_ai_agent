from sqlalchemy import Column, String, JSON, ForeignKey, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from sqlalchemy.sql import func
import uuid

class UserSession(Base):
    __tablename__ = "user_sessions"

    us_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    u_id = Column(UUID(as_uuid=True), ForeignKey("users.u_id", ondelete="CASCADE"), nullable=False)

    refresh_token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
