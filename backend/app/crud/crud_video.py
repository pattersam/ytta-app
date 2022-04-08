import logging

from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import exc
from sqlalchemy.orm import Session
from pytube import YouTube

from app.crud.base import CRUDBase
from app.models.video import Video
from app.rekognition import analyse_youtube_video
from app.schemas.video import VideoBase, VideoCreate, VideoUpdate


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_analyse_youtube_video(video: VideoBase):
    yt = YouTube(video.url)
    result = analyse_youtube_video(yt)
    video.status = result
    return video


def create_new_video(url: str) -> VideoBase:
    yt = YouTube(url)
    video = VideoBase(
        title=yt.title,
        description=yt.description,
        url=url,
        yt_id=yt.video_id,
        status='started'
    )
    return video


class CRUDVideo(CRUDBase[Video, VideoCreate, VideoUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: VideoCreate, owner_id: int,
        run_analysis: bool = True
    ) -> Video:
        new_video_data = jsonable_encoder(create_new_video(obj_in.url))
        db_obj = self.model(**new_video_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        if run_analysis:
            run_analyse_youtube_video(db_obj)
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
