from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models import ItemCreate, ItemResponse
from app.storage import InMemoryStorage
from app.dependencies import get_storage, verify_positive_id

router = APIRouter(prefix="/items", tags=["items"])

@router.post("/", response_model=ItemResponse)
def create_item(item: ItemCreate, storage: InMemoryStorage = Depends(get_storage)):
    return storage.create(item)

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int = Depends(verify_positive_id), storage: InMemoryStorage = Depends(get_storage)):
    item = storage.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    item: ItemCreate,
    storage: InMemoryStorage = Depends(get_storage),
):
    # BUG: verify_positive_id is not applied here, so id 0 is allowed
    updated = storage.update(item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@router.delete("/{item_id}")
def delete_item(item_id: int = Depends(verify_positive_id), storage: InMemoryStorage = Depends(get_storage)):
    if not storage.delete(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"ok": True}

@router.get("/", response_model=List[ItemResponse])
def list_items(storage: InMemoryStorage = Depends(get_storage)):
    # BUG: returns a dict instead of a list (type mismatch)
    # Should be: return storage.list_all()
    return storage.list_all()




