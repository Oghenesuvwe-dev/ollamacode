from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.models import Run, Finding
from sqlmodel import Session, select

def test_create_review(client: TestClient, session: Session):
    payload = {
        "repo_name": "test/repo",
        "pr_number": 101,
        "diff": "def foo(): return 1",
        "findings": [
            {
                "file_path": "main.py",
                "line_number": 10,
                "tool_name": "semgrep",
                "severity": "ERROR",
                "message": "Bad code"
            }
        ]
    }

    # Mock the Ollama generation
    with patch("app.api.generate_review", new_callable=AsyncMock) as mock_generate:
        mock_generate.return_value = "LGTM with minor nits."
        
        response = client.post("/api/v1/review", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["ai_review"] == "LGTM with minor nits."
        
        # Verify DB side effects (if we implemented DB storage in api.py)
        # For now, api.py has commented out DB logic, so we skip DB assertions
        # until that is uncommented/implemented.

def test_generate_fix(client: TestClient):
    params = {
        "filename": "broken.py",
        "content": "def broken(): pass",
        "line": 5,
        "context": "Make it work"
    }
    
    response = client.post("/api/v1/fix", params=params)
    assert response.status_code == 200
    data = response.json()
    assert "explanation" in data
    assert "code" in data
