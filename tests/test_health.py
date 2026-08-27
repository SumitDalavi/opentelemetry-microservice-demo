import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from OTel Demo"}

@patch("src.main.requests.get")
def test_call_downstream_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"message": "Hello from OTel Demo"}
    
    response = client.get("/chained")
    assert response.status_code == 200
    assert response.json() == {
        "downstream_status": 200,
        "downstream_data": {"message": "Hello from OTel Demo"}
    }
    mock_get.assert_called_once_with("http://localhost:8000/")

@patch("src.main.requests.get")
def test_call_downstream_error(mock_get):
    mock_get.side_effect = Exception("Connection refused")
    
    response = client.get("/chained")
    assert response.status_code == 200
    assert response.json() == {"error": "Connection refused"}
