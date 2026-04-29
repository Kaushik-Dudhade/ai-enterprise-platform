from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.get("/login")
def login_check():
    return {"message": "Login route initialized"}