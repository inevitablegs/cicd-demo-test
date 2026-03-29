from typing import Dict, Optional
from .models import ItemResponse, ItemCreate

class InMemoryStorage:
    def __init__(self):
        self._items: Dict[int, ItemResponse] = {}
        self._counter = 1

    def create(self, item: ItemCreate) -> ItemResponse:
        new_id = self._counter
        self._counter += 1
        new_item = ItemResponse(id=new_id, **item.model_dump())
        self._items[new_id] = new_item
        return new_item

    def get(self, item_id: int) -> Optional[ItemResponse]:
        return self._items.get(item_id)

    def update(self, item_id: int, item: ItemCreate) -> Optional[ItemResponse]:
        if item_id not in self._items:
            return None

        updated_item = ItemResponse(id=item_id, **item.model_dump())
        self._items[item_id] = updated_item
        return updated_item

    def delete(self, item_id: int) -> bool:
        if item_id in self._items:
            del self._items[item_id]
            return True
        return False

    def list_all(self) -> list[ItemResponse]:
        return list(self._items.values())