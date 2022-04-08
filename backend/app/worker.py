import logging
from typing import Optional

from sqlalchemy.orm import Session
from pytube import YouTube

from app import crud
from app.db.session import SessionLocal
from app.core.celery_app import celery_app
from app.core.config import settings
from app.rekognition import analyse_youtube_video

logger = logging.getLogger(__name__)


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"Recieved word: {word}"


@celery_app.task(acks_late=True)
def analyse_video(video_id: int, test_db: Optional[Session] = None) -> str:
    # in unit tests we need to use an existing db session, but under normal
    # operation we create a new one. Not sure on the right / elegant way to
    # manage this, but the below works.
    if test_db is None:
        db = SessionLocal()
    else:
        db = test_db
    try:
        video = crud.video.get(db, id=video_id)
        if video is None:
            raise ValueError(f"Cannot find video: {video_id}")
        logger.info(f"Analysing {video_id}. Starting status is {video.status}")
        yt = YouTube(video.url)
        result = analyse_youtube_video(yt)
        logger.info(f"Analyse of {video_id} complete. Resulting status is {result}")
        video.status = result
        db.commit()
        db.refresh(video)
        return f"Analysis of video {video_id} completed with status: {result}"
    finally:
        if test_db is None:
            db.close()
