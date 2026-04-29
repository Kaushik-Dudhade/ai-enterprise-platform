from fastapi import APIRouter
from backend.app.api.v1.auth import auth_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)

@router.get("/health")
def health_check():
    return {"status": "healthy", "version": "v1"}