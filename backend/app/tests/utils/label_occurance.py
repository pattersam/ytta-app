import random

from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.label_occurance import LabelOccuranceCreate
from app.tests.utils.label import create_random_label
from app.tests.utils.video import create_random_video


def create_random_label_occurance(
    db: Session,
    *,
    owner_id: Optional[int] = None,
    label_id: Optional[int] = None,
    video_id: Optional[int] = None
) -> models.Label:
    if label_id is None:
        label_id = create_random_label(db).id
    if video_id is None:
        video_id = create_random_video(db, owner_id=owner_id).id
    label_occurance_in = LabelOccuranceCreate(num_occurances=10, avg_confidence=50.0)
    return crud.label_occurance.create(
        db=db, obj_in=label_occurance_in, label_id=label_id, video_id=video_id
    )
