from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests.utils.user import create_random_user, authentication_token_from_email
from app.tests.utils.video import create_random_video


def test_create_video(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {
        "title": "Tired of being a bird?",
        "description": "Tired of being a bird?\nJust call this number and you will get help!",
        "url": "https://www.youtube.com/watch?v=LrWGxj43ACA",
        "yt_id": "LrWGxj43ACA",
        "status": "analysis_running",
        }
    response = client.post(
        f"{settings.API_V1_STR}/videos/", headers=superuser_token_headers, json={"url": data["url"]},
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert content["status"] == data["status"]
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
    assert content["status"] == video.status


def test_read_video_that_doesnt_exist(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/videos/-1", headers=superuser_token_headers,
    )
    assert response.status_code == 404


def test_read_video_normal_user_not_owner(
    client: TestClient, random_user_token_headers: dict, db: Session
) -> None:
    video = create_random_video(db)
    response = client.get(
        f"{settings.API_V1_STR}/videos/{video.id}", headers=random_user_token_headers,
    )
    assert response.status_code == 400


def test_read_videos_superuser(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    create_random_video(db)
    create_random_video(db)
    response = client.get(
        f"{settings.API_V1_STR}/videos",
        headers=superuser_token_headers,
        params={"limit": 2}
    )
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == 2


def test_read_videos_normal_user(
    client: TestClient, db: Session
) -> None:
    user = create_random_user(db)
    create_random_video(db, owner_id=user.id)
    response = client.get(
        f"{settings.API_V1_STR}/videos", headers=authentication_token_from_email(client=client, email=user.email, db=db)
    )
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == 1


def test_read_videos_new_user_with_no_videos(
    client: TestClient, random_user_token_headers: dict, db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/videos", headers=random_user_token_headers
    )
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == 0


def test_update_video(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    video = create_random_video(db)
    data = {"title": "new title"}
    response = client.put(
        f"{settings.API_V1_STR}/videos/{video.id}", headers=superuser_token_headers, json=data
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == video.description
    assert content["url"] == video.url
    assert content["yt_id"] == video.yt_id
    assert content["id"] == video.id
    assert content["owner_id"] == video.owner_id


def test_update_video_normal_user_not_owner(
    client: TestClient, random_user_token_headers: dict, db: Session
) -> None:
    video = create_random_video(db)
    data = {"title": "new title"}
    response = client.put(
        f"{settings.API_V1_STR}/videos/{video.id}", headers=random_user_token_headers, json=data
    )
    assert response.status_code == 400


def test_update_video_that_doesnt_exist(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {
        "title": "new title",
        }
    response = client.put(
        f"{settings.API_V1_STR}/videos/-1", headers=superuser_token_headers, json=data
    )
    assert response.status_code == 404


def test_delete_video(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    video = create_random_video(db)
    response = client.delete(
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
    response2 = client.delete(
        f"{settings.API_V1_STR}/videos/{video.id}", headers=superuser_token_headers,
    )
    assert response2.status_code == 404


def test_delete_video_that_doesnt_exist(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/videos/-1", headers=superuser_token_headers,
    )
    assert response.status_code == 404


def test_delete_video_normal_user_not_owner(
    client: TestClient, random_user_token_headers: dict, db: Session
) -> None:
    video = create_random_video(db)
    response = client.delete(
        f"{settings.API_V1_STR}/videos/{video.id}", headers=random_user_token_headers,
    )
    assert response.status_code == 400
