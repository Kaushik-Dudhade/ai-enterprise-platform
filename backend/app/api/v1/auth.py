from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from backend.app.db.session import SessionLocal
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserLogin
from backend.app.core.security import hash_password, verify_password, create_access_token, verify_access_token

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload["sub"]



@auth_router.get("/login")
def login_check():
    return {"message": "Login route initialized"}

@auth_router.post("/create-user")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user_id": new_user.id,
        "email": new_user.email
    }

@auth_router.post("/login-user")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({"sub": existing_user.email})

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }


@auth_router.get("/me")
def get_my_profile(current_user: str = Depends(get_current_user)):
    return {
        "message": "Protected profile data accessed",
        "logged_in_as": current_user
    }