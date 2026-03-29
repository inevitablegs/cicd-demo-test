from fastapi import FastAPI
from app.routers import items

app = FastAPI(title="Demo API", version="1.0.0")

app.include_router(items.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

# BUG: missing import for HTTPException is not needed here, but we intentionally
# leave a syntax-like error? Actually no, but we can add a harmless unused import.
# However we need at least one error that will be caught by linting: unused variable.
def unused_function():
    x = 42   # ruff will flag unused variable