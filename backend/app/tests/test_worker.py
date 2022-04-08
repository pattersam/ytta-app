from sqlalchemy.orm import Session

from app import crud
from app import worker
from app.schemas.video import VideoCreate, VideoUpdate
from app.tests.utils.video import create_random_video


def test_test_celery(db: Session) -> None:
    word = "hello"
    analysis_results = worker.test_celery(word)
    assert analysis_results == f"Recieved word: {word}"


def test_analyse_video(db: Session) -> None:
    video = create_random_video(db)
    analysis_results = worker.analyse_video(video.id, test_db=db)
    assert (
        analysis_results
        == f"Analysis of video {video.id} completed with status: success"
    )
