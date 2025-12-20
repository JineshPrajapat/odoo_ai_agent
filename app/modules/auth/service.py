from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.schemas.user_session import UserSessionCreate
from app.crud.user import UserRepository
from app.crud.user_session import UserSessionRepository
from app.modules.auth.jwt import create_access_token, create_refresh_token
from app.modules.auth.security import (
    hash_password,
    verify_password,
    generate_refresh_token,
    refresh_token_expiry,
)

class AuthService:

    @staticmethod
    def register(db: Session, payload: UserCreate):
        existing = UserRepository.get_by_email(db, payload.email)
        if existing:
            raise ValueError("User already exists")

        password_hash = hash_password(payload.password)
        return UserRepository.create(db, payload, password_hash)

    @staticmethod
    def login(db: Session, email: str, password: str):
        user = UserRepository.get_by_email(db, email)
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        access_token, access_exp = create_access_token(str(user.u_id))
        refresh_token, refresh_exp = create_refresh_token(str(user.u_id))

        session_payload = UserSessionCreate(
            u_id=user.u_id,
            refresh_token=refresh_token,
            expires_at=refresh_exp,
        )
        UserSessionRepository.create(db, session_payload)

        return {
            "access_token": access_token,
            "access_token_expires_at": access_exp,
            "refresh_token": refresh_token,
            "refresh_token_expires_at": refresh_exp,
            "token_type": "Bearer",
        }
