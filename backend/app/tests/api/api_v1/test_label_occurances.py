from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.label_occurance import create_random_label_occurance


def test_read_labels(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    create_random_label_occurance(db)
    create_random_label_occurance(db)
    response = client.get(
        f"{settings.API_V1_STR}/label_occurances",
        headers=superuser_token_headers,
        params={"limit": 2},
    )
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == 2
