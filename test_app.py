import pytest
import json
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_handle_request_not_json(client):
    response = client.post('/api-endpoint', data="not json")
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert response_data["error"] == "Request must be JSON"

def test_handle_request_missing_field(client):
    response = client.post('/api-endpoint', json={})
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert "Missing field" in response_data["error"]

def test_handle_request_invalid_secret(client):
    data = {
        "email": "student@example.com",
        "secret": "invalid-secret",
        "task": "captcha-solver-...",
        "round": 1,
        "nonce": "ab12-...",
        "brief": "Create a captcha solver that handles ?url=https://.../image.png. Default to attached sample.",
        "checks": [],
        "evaluation_url": "https://example.com/notify"
    }
    response = client.post('/api-endpoint', json=data)
    assert response.status_code == 403
    response_data = json.loads(response.data)
    assert response_data["error"] == "Invalid secret"

def test_handle_request_round_1_success(client, monkeypatch):
    # Mock the GITHUB_TOKEN environment variable
    monkeypatch.setenv("GITHUB_TOKEN", "test-token")

    data = {
        "email": "student@example.com",
        "secret": "my-super-secret-key",
        "task": "sum-of-sales-test",
        "round": 1,
        "nonce": "ab12-...",
        "brief": "sum-of-sales",
        "checks": [],
        "evaluation_url": "https://example.com/notify",
        "attachments": [{ "name": "data.csv", "url": "data:text/csv;base64,cHJvZHVjdCx_c2FsZXMKZm9vLDEwCmJhciwyMA==" }]
    }

    # Mock the build_and_deploy function to avoid actual GitHub API calls
    def mock_build_and_deploy(data):
        pass

    monkeypatch.setattr("app.build_and_deploy", mock_build_and_deploy)

    response = client.post('/api-endpoint', json=data)
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["status"] == "build-started"