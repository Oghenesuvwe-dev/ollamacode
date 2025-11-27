from fastapi.testclient import TestClient

def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "OllamaCode Backend is running"}

# Note: We are mocking the Ollama call in a real test suite
# For now, we just test the endpoint structure if we had a mock
