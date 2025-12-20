from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str | None = None
    role: str | None = "user"
    is_active: bool | None = True

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
        
# class UserRead(UserBase):
#     u_id: UUID
#     created_at: datetime
#     updated_at: datetime | None = None

#     class Config:
#         from_attributes = True  # important to read from SQLAlchemy model

# class UserUpdate(BaseModel):
#     name: str | None
#     role: str | None
#     is_active: bool | None
