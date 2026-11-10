from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
HEADERS = {"X-API-Key": "quantum-factory-secret-2026"}

def test_router():
    response = client.post("/api/v1/router/predict", json={"query": "write a python script"}, headers=HEADERS)
    assert response.status_code == 200
    assert "tier" in response.json()