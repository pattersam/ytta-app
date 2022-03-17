from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "YouTube Tag Analyser API"}

def test_non_existing_resource():
    response = client.get("/bad")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

def test_get_videos():
    response = client.get("/videos")
    assert response.status_code == 200
    assert response.json() == {"msg": "TO BE IMPLEMENTED"}

def test_get_video():
    response = client.get("/videos/aaabbb")
    assert response.status_code == 200
    assert response.json() == {"msg": "TO BE IMPLEMENTED aaabbb"}

def test_post_videos():
    response = client.post("/videos/?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DykwyamBDUu8")
    assert response.status_code == 200
    assert response.json() == {
        "msg": "Download finished",
        "fname": "/workspace/ytta-app/downloads/[ykwyamBDUu8] Tired of Being a Bird.mp4"
        }
