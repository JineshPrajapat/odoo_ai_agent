from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from app.core.config import DATABASE_URL

engine =  create_engine(
    DATABASE_URL, 
    future=True,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    bind=engine, 
    autoflush=False,
    autocommit=False
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()