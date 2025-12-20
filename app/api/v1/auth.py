from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.service import AuthService
from app.schemas.user import UserCreate, UserResponse
from app.schemas.user_session import UserSessionBase

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        return AuthService.register(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=UserSessionBase)
def login(email: str, password: str, db: Session = Depends(get_db)):
    try:
        return AuthService.login(db, email, password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
