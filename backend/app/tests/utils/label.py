import random

from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.label import LabelCreate
from app.tests.utils.utils import random_lower_string


def create_random_label(
    db: Session, *, owner_id: Optional[int] = None, run_analysis: bool = False
) -> models.Label:
    name = random_lower_string()
    label_in = LabelCreate(name=name)
    return crud.label.create(db=db, obj_in=label_in)
