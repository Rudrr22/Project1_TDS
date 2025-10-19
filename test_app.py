from fastapi.testclient import TestClient
from app import app
import json

client = TestClient(app)

def test_execute_get_ticket_status():
    response = client.get("/execute?q=What is the status of ticket 83742?")
    assert response.status_code == 200
    expected_data = {
        "name": "get_ticket_status",
        "arguments": json.dumps({"ticket_id": 83742}),
    }
    assert response.json() == expected_data

def test_execute_not_implemented():
    response = client.get("/execute?q=some other query")
    assert response.status_code == 200
    expected_data = {"name": "not_implemented", "arguments": "{}"}
    assert response.json() == expected_data
