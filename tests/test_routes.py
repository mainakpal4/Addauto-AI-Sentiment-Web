from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

client = TestClient(app)

def test_analyze_text_valid():
    response = client.post("/analyze", json={"text": "I love this project!"})
    assert response.status_code == 200
    data = response.json()
    assert "emotion" in data
    assert "confidence" in data
    assert isinstance(data["emotion"], str)
    assert isinstance(data["confidence"], float)

def test_analyze_text_empty_input():
    response = client.post("/analyze", json={"text": ""})
    assert response.status_code == 200  # Your mock will still return success
    data = response.json()
    assert "emotion" in data
    assert "confidence" in data

def test_analyze_text_missing_field():
    response = client.post("/analyze", json={})
    assert response.status_code == 422  # Unprocessable Entity due to missing field
