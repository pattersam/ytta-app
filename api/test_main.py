from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "YouTube Tag Analyser API"}

def test_read_non_existing_resource():
    response = client.get("/bad")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

