from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    price: float    # intentionally correct type, but we'll break later
    in_stock: bool

class ItemResponse(ItemCreate):
    id: int