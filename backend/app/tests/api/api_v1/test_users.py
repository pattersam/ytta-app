from cProfile import label
from typing import Dict

from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.tests.utils.utils import random_email, random_lower_string
from app.tests.utils.user import create_random_user
from app.tests.utils.video import create_random_video
from app.tests.utils.label import create_random_label
from app.tests.utils.label_occurance import create_random_label_occurance


def test_get_users_superuser_me(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


def test_get_users_normal_user_me(
    client: TestClient, normal_user_token_headers: Dict[str, str], db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER


def test_create_user_new_email(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.user.get_by_email(db, email=username)
    assert user
    assert user.email == created_user["email"]


def test_get_existing_user(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    user_id = user.id
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}", headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.user.get_by_email(db, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_create_user_existing_username(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_email()
    # username = email
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    crud.user.create(db, obj_in=user_in)
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


def test_create_user_by_normal_user(
    client: TestClient, normal_user_token_headers: Dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=normal_user_token_headers, json=data,
    )
    assert r.status_code == 400


def test_create_user_by_random_user(
    client: TestClient, random_user_token_headers: Dict[str, str],  db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=random_user_token_headers, json=data,
    )
    assert r.status_code == 400


def test_retrieve_users(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    crud.user.create(db, obj_in=user_in)

    username2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    crud.user.create(db, obj_in=user_in2)

    r = client.get(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers)
    all_users = r.json()

    assert len(all_users) > 1
    for item in all_users:
        assert "email" in item


def test_update_user(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    data = {"full_name": "Updated Full Name"}
    r = client.put(
        f"{settings.API_V1_STR}/users/{user.id}", headers=superuser_token_headers, json=data,
    )
    assert r.status_code == 200
    updated_user = r.json()
    assert updated_user
    assert updated_user["full_name"] == data["full_name"]


def test_update_user_that_doesnt_exist(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"full_name": "Updated Full Name"}
    r = client.put(
        f"{settings.API_V1_STR}/users/-1", headers=superuser_token_headers, json=data,
    )
    assert r.status_code == 404


def test_get_users_videos(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    video = create_random_video(db, owner_id=user.id)
    r = client.get(
        f"{settings.API_V1_STR}/users/{user.id}/videos", headers=superuser_token_headers,
    )
    assert 200 == r.status_code
    videos = r.json()
    assert len(videos) == 1
    assert jsonable_encoder(videos) == jsonable_encoder([video])


def test_get_users_label_occurances(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    video = create_random_video(db, owner_id=user.id)
    lo1 = jsonable_encoder(create_random_label_occurance(db, video_id=video.id))
    lo2 = jsonable_encoder(create_random_label_occurance(db, video_id=video.id))
    r = client.get(
        f"{settings.API_V1_STR}/users/{user.id}/label_occurances", headers=superuser_token_headers,
    )
    assert 200 == r.status_code
    label_occurances = r.json()
    assert len(label_occurances) == 2
    assert jsonable_encoder(label_occurances) == [lo1, lo2]


def test_get_users_label_occurances_with_label_name(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    video = create_random_video(db, owner_id=user.id)
    label1 = create_random_label(db)
    label2 = create_random_label(db)
    create_random_label_occurance(db, label_id=label1.id, video_id=video.id)
    create_random_label_occurance(db, label_id=label2.id, video_id=video.id)
    r = client.get(
        f"{settings.API_V1_STR}/users/{user.id}/label_occurances",
        headers=superuser_token_headers,
        params={"with_label_names": True},
    )
    assert 200 == r.status_code
    label_occurances = r.json()
    print(label_occurances)
    assert len(label_occurances) == 2
    assert {l["label_name"] for l in label_occurances} == {label1.name, label2.name}
