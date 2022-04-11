from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.label import create_random_label


def test_create_label(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {
        "name": "Bird",
    }
    response = client.post(
        f"{settings.API_V1_STR}/labels/",
        headers=superuser_token_headers,
        json={"name": data["name"]},
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert "id" in content


def test_read_label(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    label = create_random_label(db)
    response = client.get(
        f"{settings.API_V1_STR}/labels/{label.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == label.name


def test_read_label_that_doesnt_exist(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/labels/-1",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404


def test_read_labels(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    create_random_label(db)
    create_random_label(db)
    response = client.get(
        f"{settings.API_V1_STR}/labels",
        headers=superuser_token_headers,
        params={"limit": 2},
    )
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == 2


def test_update_label(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    label = create_random_label(db)
    data = {"name": "new name"}
    response = client.put(
        f"{settings.API_V1_STR}/labels/{label.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]


def test_update_label_that_doesnt_exist(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {
        "name": "new name",
    }
    response = client.put(
        f"{settings.API_V1_STR}/labels/-1", headers=superuser_token_headers, json=data
    )
    assert response.status_code == 404
