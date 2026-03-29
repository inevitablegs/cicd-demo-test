from fastapi import FastAPI, Depends
from app.dependencies import get_settings
from app.routers import items

app = FastAPI(title="Production FastAPI Demo")

app.include_router(items.router, prefix="/api/items", tags=["items"])

@app.get("/health")
def health(settings = Depends(get_settings)):
    return {"status": "ok", "environment": settings.environment}