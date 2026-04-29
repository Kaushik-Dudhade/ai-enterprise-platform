from fastapi import FastAPI
from backend.app.api.routes import router
from backend.app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.include_router(router)

@app.get("/")
def home():
    return {
        "message": settings.APP_NAME,
        "version": settings.APP_VERSION
    }