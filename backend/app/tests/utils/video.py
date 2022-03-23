import random

from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.video import VideoCreate
from app.tests.utils.user import create_random_user


youtube_video_urls = [
    'https://www.youtube.com/watch?v=1mA7BbliyL8',
    'https://www.youtube.com/watch?v=nEywOaEcIQs',
]

def get_random_youtube_video_url():
    return random.choice(youtube_video_urls)

def create_random_video(db: Session, *, owner_id: Optional[int] = None) -> models.Video:
    if owner_id is None:
        user = create_random_user(db)
        owner_id = user.id
    url = get_random_youtube_video_url()
    video_in = VideoCreate(url=url)
    return crud.video.create_with_owner(db=db, obj_in=video_in, owner_id=owner_id)
