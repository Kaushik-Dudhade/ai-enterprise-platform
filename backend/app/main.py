from fastapi import FastAPI
from backend.app.api.routes import router
from backend.app.core.config import settings
from backend.app.db.session import engine, Base
from backend.app.models import user

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def home():
    return {
        "message": settings.APP_NAME,
        "version": settings.APP_VERSION
    }