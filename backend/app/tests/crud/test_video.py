from sqlalchemy.orm import Session

from app import crud
from app.schemas.video import VideoCreate, VideoUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.video import get_random_youtube_video_url
from app.tests.utils.utils import random_lower_string


def test_create_video(db: Session) -> None:
    title = 'I finally got my big break'
    url = 'https://www.youtube.com/watch?v=Yw_LprMOygw'
    yt_id = 'Yw_LprMOygw'
    video_in = VideoCreate(url=url)
    user = create_random_user(db)
    video = crud.video.create_with_owner(db=db, obj_in=video_in, owner_id=user.id)
    assert video.title == title
    assert video.url == url
    assert video.yt_id == yt_id
    assert video.owner_id == user.id
    assert video.status == 'analysis_running'


def test_create_video_without_starting_analysis(db: Session) -> None:
    title = 'I finally got my big break'
    url = 'https://www.youtube.com/watch?v=Yw_LprMOygw'
    yt_id = 'Yw_LprMOygw'
    video_in = VideoCreate(url=url)
    user = create_random_user(db)
    video = crud.video.create_with_owner(db=db, obj_in=video_in, owner_id=user.id, run_analysis=False)
    assert video.title == title
    assert video.url == url
    assert video.yt_id == yt_id
    assert video.owner_id == user.id
    assert video.status == 'created'


def test_get_video(db: Session) -> None:
    url = get_random_youtube_video_url()
    user = create_random_user(db)
    video = crud.video.create_with_owner(db=db, obj_in=VideoCreate(url=url), owner_id=user.id, run_analysis=False)
    stored_video = crud.video.get(db=db, id=video.id)
    assert stored_video
    assert video.id == stored_video.id
    assert video.title == stored_video.title
    assert video.description == stored_video.description
    assert video.url == stored_video.url
    assert video.yt_id == stored_video.yt_id
    assert video.owner_id == stored_video.owner_id


def test_get_multo_video(db: Session) -> None:
    url = get_random_youtube_video_url()
    user = create_random_user(db)
    video = crud.video.create_with_owner(db=db, obj_in=VideoCreate(url=url), owner_id=user.id, run_analysis=False)
    stored_videos = crud.video.get_multi_by_owner(db=db, owner_id=user.id, skip=0, limit=100)
    stored_video = stored_videos[0]
    assert stored_videos
    assert len(stored_videos) == 1
    assert video.id == stored_video.id
    assert video.title == stored_video.title
    assert video.description == stored_video.description
    assert video.url == stored_video.url
    assert video.yt_id == stored_video.yt_id
    assert video.owner_id == stored_video.owner_id


def test_update_video(db: Session) -> None:
    url = get_random_youtube_video_url()
    user = create_random_user(db)
    video = crud.video.create_with_owner(db=db, obj_in=VideoCreate(url=url), owner_id=user.id, run_analysis=False)
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
    url = get_random_youtube_video_url()
    user = create_random_user(db)
    video = crud.video.create_with_owner(db=db, obj_in=VideoCreate(url=url), owner_id=user.id, run_analysis=False)
    video2 = crud.video.remove(db=db, id=video.id)
    video3 = crud.video.get(db=db, id=video.id)
    assert video3 is None
    assert video2.id == video.id
    assert video2.url == url
    assert video2.title == video.title
    assert video2.description == video.description
    assert video2.owner_id == user.id
