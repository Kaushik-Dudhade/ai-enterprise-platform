from fastapi import FastAPI
from backend.app.api.routes import router

app = FastAPI(title="AI Enterprise Platform")

app.include_router(router)

@app.get("/")
def home():
    return {"message": "AI Enterprise Platform Running"}