from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.video import VideoCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_video(db: Session, *, owner_id: Optional[int] = None) -> models.Video:
    if owner_id is None:
        user = create_random_user(db)
        owner_id = user.id
    title = random_lower_string()
    description = random_lower_string()
    url = random_lower_string()
    yt_id = random_lower_string()
    video_in = VideoCreate(title=title, description=description, url=url, yt_id=yt_id, id=id)
    return crud.video.create_with_owner(db=db, obj_in=video_in, owner_id=owner_id)
