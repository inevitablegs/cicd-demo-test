from fastapi import HTTPException
from .storage import InMemoryStorage

storage = InMemoryStorage()
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Demo API"
    debug: bool = True

def get_settings():
    return Settings()

def get_storage():
    return storage

def verify_positive_id(item_id: int) -> int:
    # BUG: division by zero when item_id == 0
    # Should be: if item_id <= 0: raise HTTPException(...)
    result = 100 / item_id   # raises ZeroDivisionError for id 0
    if result <= 0:
        raise HTTPException(status_code=400, detail="ID must be positive")
    return item_id