from sqlalchemy.orm import Session
from app.models.user_sessions import UserSession
from app.schemas.user_session import UserSessionCreate

class UserSessionRepository:
    def create(db: Session, payload: UserSessionCreate) -> UserSession:
        session = UserSession(
            u_id_id=payload.u_id,
            refresh_token=payload.refresh_token,
            expires_at=payload.expires_at,
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
