import asyncio
import sys
import os

# Add backend directory to path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi.testclient import TestClient
from src.main import app

def test_store_api():
    client = TestClient(app)

    print("--- 1. Testing GET /api/store/products ---")
    res = client.get("/api/store/products")
    print("Status:", res.status_code)
    assert res.status_code == 200
    products = res.json()
    print("Products count:", len(products))
    print("Sample product:", products[0])

    print("\n--- 2. Testing GET /api/store/products/1 ---")
    res = client.get("/api/store/products/1")
    print("Status:", res.status_code)
    assert res.status_code == 200
    p1 = res.json()
    print("Product #1:", p1["name"], "- Stock:", p1["stock"])

    print("\n--- 3. Testing POST /api/store/orders (Stock Error) ---")
    bad_payload = {
        "customer": {
            "name": "Jane Doe",
            "address": "456 Market St",
            "email": "jane@example.com",
            "phone": "+1 555-0199"
        },
        "items": [
            {"product_id": 4, "quantity": 9999}
        ]
    }
    res = client.post("/api/store/orders", json=bad_payload)
    print("Status:", res.status_code)
    assert res.status_code == 400
    print("Error response:", res.json())

    print("\n--- 4. Testing POST /api/store/orders (Successful Placement) ---")
    valid_payload = {
        "customer": {
            "name": "Alice Smith",
            "address": "123 Main St",
            "email": "alice@example.com",
            "phone": "+1 555-0100"
        },
        "items": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 3, "quantity": 1}
        ]
    }
    res = client.post("/api/store/orders", json=valid_payload)
    print("Status:", res.status_code)
    assert res.status_code == 200
    order_data = res.json()
    print("Order Confirmation:", order_data)
    assert order_data["status"] == "success"
    assert order_data["order_id"].startswith("ORD-")
    assert order_data["total"] == round(129.99 * 2 + 69.99 * 1, 2)
    print("\n[SUCCESS] All Store API verification tests PASSED!")

if __name__ == "__main__":
    test_store_api()
