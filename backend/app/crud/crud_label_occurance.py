from typing import Any, Dict, Optional, Union, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.label_occurance import LabelOccurance
from app.schemas.label_occurance import LabelOccuranceCreate, LabelOccuranceUpdate


class CRUDLabelOccurance(
    CRUDBase[LabelOccurance, LabelOccuranceCreate, LabelOccuranceUpdate]
):
    def create(
        self,
        db: Session,
        *,
        obj_in: LabelOccuranceCreate,
        label_id: int,
        video_id: int,
    ) -> LabelOccurance:
        new_label_occurance_data = jsonable_encoder(obj_in)
        db_obj = self.model(
            **new_label_occurance_data, label_id=label_id, video_id=video_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_video(
        self, db: Session, *, video_id: int, skip: int = 0, limit: int = 100
    ) -> List[LabelOccurance]:
        return (
            db.query(self.model)
            .filter(LabelOccurance.video_id == video_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_label(
        self, db: Session, *, label_id: int, skip: int = 0, limit: int = 100
    ) -> List[LabelOccurance]:
        return (
            db.query(self.model)
            .filter(LabelOccurance.label_id == label_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_label_and_video(
        self,
        db: Session,
        *,
        label_id: int,
        video_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> List[LabelOccurance]:
        return (
            db.query(self.model)
            .filter(LabelOccurance.label_id == label_id)
            .filter(LabelOccurance.video_id == video_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


label_occurance = CRUDLabelOccurance(LabelOccurance)
