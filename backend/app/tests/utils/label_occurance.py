import random

from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.label_occurance import LabelOccuranceCreate
from app.tests.utils.label import create_random_label
from app.tests.utils.video import create_random_video


def create_random_label_occurance(
    db: Session, *, owner_id: Optional[int] = None, run_analysis: bool = False
) -> models.Label:
    label = create_random_label(db)
    video = create_random_video(db)
    label_occurance_in = LabelOccuranceCreate(num_occurances=10, avg_confidence=50.0)
    return crud.label_occurance.create(
        db=db, obj_in=label_occurance_in, label_id=label.id, video_id=video.id
    )
