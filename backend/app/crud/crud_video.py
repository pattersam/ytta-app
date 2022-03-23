import logging

from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import exc
from sqlalchemy.orm import Session
from pytube import YouTube

from app.crud.base import CRUDBase
from app.models.video import Video
from app.schemas.video import VideoBase, VideoCreate, VideoUpdate


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_new_video(url: str) -> VideoBase:
    yt = YouTube(url)
    # logger.info(f"Downloading: {url}")
    # yt.streams.filter(only_video=True, file_extension='mp4').first().download('downloads/', filename_prefix=f"[{yt.video_id}] ")
    return VideoBase(
        title=yt.title,
        description=yt.description,
        url=url,
        yt_id=yt.video_id,
    )


class CRUDVideo(CRUDBase[Video, VideoCreate, VideoUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: VideoCreate, owner_id: int
    ) -> Video:
        new_video_data = jsonable_encoder(create_new_video(obj_in.url))
        db_obj = self.model(**new_video_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Video]:
        return (
            db.query(self.model)
            .filter(Video.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


video = CRUDVideo(Video)
