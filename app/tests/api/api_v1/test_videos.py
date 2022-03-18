from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.video import create_random_video


def test_create_video(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {
        "title": "Tired of Being a Bird?",
        "description": "Tired of Being a Bird?",
        "url": "https://www.youtube.com/watch?v=ykwyamBDUu8",
        "yt_id": "ykwyamBDUu8",
        }
    response = client.post(
        f"{settings.API_V1_STR}/videos/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


def test_read_video(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    video = create_random_video(db)
    response = client.get(
        f"{settings.API_V1_STR}/videos/{video.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == video.title
    assert content["description"] == video.description
    assert content["url"] == video.url
    assert content["yt_id"] == video.yt_id
    assert content["id"] == video.id
    assert content["owner_id"] == video.owner_id
