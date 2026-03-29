import pytest
from fastapi.testclient import TestClient
from app.main import app

from app.dependencies import get_storage
from app.storage import InMemoryStorage


@pytest.fixture()
def client():
    storage = InMemoryStorage()
    app.dependency_overrides[get_storage] = lambda: storage
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

def test_create_and_get_item(client: TestClient):
    # Create
    resp = client.post("/items/", json={"name": "book", "price": 12.99, "in_stock": True})
    assert resp.status_code == 200
    data = resp.json()
    item_id = data["id"]
    assert data["name"] == "book"
    assert data["price"] == 12.99

    # Get
    resp = client.get(f"/items/{item_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "book"

def test_update_item(client: TestClient):
    # Create
    resp = client.post("/items/", json={"name": "pen", "price": 1.50, "in_stock": True})
    item_id = resp.json()["id"]
    # Update
    resp = client.put(
        f"/items/{item_id}",
        json={"name": "pen (updated)", "price": 1.75, "in_stock": False}
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "pen (updated)"
    assert resp.json()["price"] == 1.75

def test_delete_item(client: TestClient):
    resp = client.post("/items/", json={"name": "eraser", "price": 0.99, "in_stock": True})
    item_id = resp.json()["id"]
    resp = client.delete(f"/items/{item_id}")
    assert resp.status_code == 200
    resp = client.get(f"/items/{item_id}")
    assert resp.status_code == 404

def test_list_items(client: TestClient):
    client.post("/items/", json={"name": "a", "price": 1, "in_stock": True})
    client.post("/items/", json={"name": "b", "price": 2, "in_stock": False})
    resp = client.get("/items/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) == 2


