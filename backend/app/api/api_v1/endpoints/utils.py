import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.celery_app import celery_app
from app.utils import send_test_email

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/test-celery/", response_model=schemas.Msg, status_code=201)
def test_celery(
    msg: schemas.Msg,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": f"Message received: {msg.msg}"}


@router.post("/analyse-video/{video_id}", response_model=schemas.Msg, status_code=201)
def analyse_video(
    video_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Run AWS Rekognition analysis.
    """
    video = crud.video.get(db, id=video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    if not crud.user.is_superuser(current_user) and (video.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    celery_app.send_task("app.worker.analyse_video", args=[video_id])
    return {"msg": f"Analysis started for video {video_id}."}


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}
