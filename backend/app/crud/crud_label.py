from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.label import Label
from app.schemas.label import LabelCreate, LabelUpdate


class CRUDLabel(CRUDBase[Label, LabelCreate, LabelUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Label]:
        return db.query(Label).filter(Label.name == name).first()


label = CRUDLabel(Label)
