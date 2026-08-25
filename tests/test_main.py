import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from OTel Demo"}

def test_chained_endpoint(monkeypatch):
    # Mock requests.get to avoid actual network call during tests
    class MockResponse:
        status_code = 200
        def json(self):
            return {"message": "Mocked response"}
            
    monkeypatch.setattr("requests.get", lambda url: MockResponse())
    
    response = client.get("/chained")
    assert response.status_code == 200
    assert response.json()["downstream_status"] == 200
    assert response.json()["downstream_data"] == {"message": "Mocked response"}
