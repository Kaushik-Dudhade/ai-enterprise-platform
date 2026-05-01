from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.db.session import SessionLocal
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@auth_router.get("/login")
def login_check():
    return {"message": "Login route initialized"}

@auth_router.post("/create-user")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user