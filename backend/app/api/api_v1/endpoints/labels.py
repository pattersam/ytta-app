from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=List[schemas.Label])
def read_labels(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve labels.
    """
    labels = crud.label.get_multi(db, skip=skip, limit=limit)
    return labels


@router.post("/", response_model=schemas.Label)
def create_label(
    *,
    db: Session = Depends(deps.get_db),
    label_in: schemas.LabelCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new label.
    """
    label = crud.label.get_by_name(db, name=label_in.name)
    if label:
        raise HTTPException(
            status_code=400,
            detail="A label with this name already exists in the system.",
        )
    label = crud.label.create(db, obj_in=label_in)
    return label


@router.get("/{label_id}", response_model=schemas.Label)
def read_user_by_id(
    label_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific label by id.
    """
    label = crud.label.get(db, id=label_id)
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    return label


@router.put("/{label_id}", response_model=schemas.Label)
def update_label(
    *,
    db: Session = Depends(deps.get_db),
    label_id: int,
    label_in: schemas.LabelUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a label.
    """
    label = crud.label.get(db, id=label_id)
    if not label:
        raise HTTPException(
            status_code=404,
            detail="The label with this id does not exist in the system",
        )
    label = crud.label.update(db, db_obj=label, obj_in=label_in)
    return label
