from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class UserSessionBase(BaseModel):
    u_id: UUID
    refresh_token: str
    expires_at: datetime

class UserSessionCreate(UserSessionBase):
    pass

# class UserSessionRead(UserSessionBase):
#     us_id: UUID
#     created_at: datetime
#     updated_at: datetime | None = None

#     class Config:
#         from_attributes = True
