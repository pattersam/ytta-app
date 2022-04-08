from typing import Dict
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient

from app.core.config import settings
from app.tests.utils.video import create_random_video


def test_celery_worker_test(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    data = {"msg": "test"}
    r = client.post(
        f"{settings.API_V1_STR}/utils/test-celery/",
        json=data,
        headers=superuser_token_headers,
    )
    response = r.json()
    assert response["msg"] == "Message received: test"


def test_analyse_video(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    video_id = create_random_video(db).id
    r = client.post(
        f"{settings.API_V1_STR}/utils/analyse-video/{video_id}",
        headers=superuser_token_headers,
    )
    response = r.json()
    assert response["msg"] == f"Analysis started for video {video_id}."
