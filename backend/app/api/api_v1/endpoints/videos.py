from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Video])
def read_videos(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve videos.
    """
    if crud.user.is_superuser(current_user):
        videos = crud.video.get_multi(db, skip=skip, limit=limit)
    else:
        videos = crud.video.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return videos


@router.post("/", response_model=schemas.Video)
def create_video(
    *,
    db: Session = Depends(deps.get_db),
    video_in: schemas.VideoCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new video.
    """
    video = crud.video.create_with_owner(db=db, obj_in=video_in, owner_id=current_user.id)
    return video


@router.put("/{id}", response_model=schemas.Video)
def update_video(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    video_in: schemas.VideoUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an video.
    """
    video = crud.video.get(db=db, id=id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    if not crud.user.is_superuser(current_user) and (video.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    video = crud.video.update(db=db, db_obj=video, obj_in=video_in)
    return video


@router.get("/{id}", response_model=schemas.Video)
def read_video(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get video by ID.
    """
    video = crud.video.get(db=db, id=id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    if not crud.user.is_superuser(current_user) and (video.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return video


@router.delete("/{id}", response_model=schemas.Video)
def delete_video(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an video.
    """
    video = crud.video.get(db=db, id=id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    if not crud.user.is_superuser(current_user) and (video.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    video = crud.video.remove(db=db, id=id)
    return video
