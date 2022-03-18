from sqlalchemy.orm import Session

from app import crud
from app.schemas.video import VideoCreate, VideoUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_video(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    url = random_lower_string()
    yt_id = random_lower_string()
    video_in = VideoCreate(title=title, description=description, url=url, yt_id=yt_id)
    user = create_random_user(db)
    video = crud.video.create_with_owner(db=db, obj_in=video_in, owner_id=user.id)
    assert video.title == title
    assert video.description == description
    assert video.url == url
    assert video.yt_id == yt_id
    assert video.owner_id == user.id


def test_get_video(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    url = random_lower_string()
    yt_id = random_lower_string()
    video_in = VideoCreate(title=title, description=description, url=url, yt_id=yt_id)
    user = create_random_user(db)
    video = crud.video.create_with_owner(db=db, obj_in=video_in, owner_id=user.id)
    stored_video = crud.video.get(db=db, id=video.id)
    assert stored_video
    assert video.id == stored_video.id
    assert video.title == stored_video.title
    assert video.description == stored_video.description
    assert video.url == stored_video.url
    assert video.yt_id == stored_video.yt_id
    assert video.owner_id == stored_video.owner_id


def test_update_video(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    url = random_lower_string()
    yt_id = random_lower_string()
    video_in = VideoCreate(title=title, description=description, url=url, yt_id=yt_id)
    user = create_random_user(db)
    video = crud.video.create_with_owner(db=db, obj_in=video_in, owner_id=user.id)
    description2 = random_lower_string()
    video_update = VideoUpdate(description=description2)
    video2 = crud.video.update(db=db, db_obj=video, obj_in=video_update)
    assert video.id == video2.id
    assert video.title == video2.title
    assert video2.description == description2
    assert video.url == video2.url
    assert video.yt_id == video2.yt_id
    assert video.owner_id == video2.owner_id


def test_delete_video(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    url = random_lower_string()
    yt_id = random_lower_string()
    video_in = VideoCreate(title=title, description=description, url=url, yt_id=yt_id)
    user = create_random_user(db)
    video = crud.video.create_with_owner(db=db, obj_in=video_in, owner_id=user.id)
    video2 = crud.video.remove(db=db, id=video.id)
    video3 = crud.video.get(db=db, id=video.id)
    assert video3 is None
    assert video2.id == video.id
    assert video2.title == title
    assert video2.description == description
    assert video2.owner_id == user.id
