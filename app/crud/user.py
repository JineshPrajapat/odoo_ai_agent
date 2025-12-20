from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

class UserRepository:
    def get_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def create(db: Session, payload: UserCreate, password: str) -> User:
        user = User(
            email=payload.email,
            name=payload.name,
            role=payload.role,
            is_active=payload.is_active,
            password=password,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
# user_repo = UserRepository()
