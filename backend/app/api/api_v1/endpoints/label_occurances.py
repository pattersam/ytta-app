from cProfile import label
from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=List[schemas.LabelOccurance])
def read_label_occurances(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    label_id: Optional[int] = None,
    video_id: Optional[int] = None,
) -> Any:
    """
    Retrieve labels.
    """
    if (label_id is None) and (video_id is None):
        labels = crud.label_occurance.get_multi(db, skip=skip, limit=limit)
    elif (label_id is not None) and (video_id is None):
        labels = crud.label_occurance.get_multi_by_label(
            db, skip=skip, limit=limit, label_id=label_id
        )
    elif (label_id is None) and (video_id is not None):
        labels = crud.label_occurance.get_multi_by_video(
            db, skip=skip, limit=limit, video_id=video_id
        )
    else:
        labels = crud.label_occurance.get_multi_by_label_and_video(
            db, skip=skip, limit=limit, label_id=label_id, video_id=video_id
        )
    return labels
