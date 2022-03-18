from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db import base


def clear_db(db: Session, dry_run: bool = True) -> None:
    if not dry_run:
        db.query(base.Video).delete()
        db.query(base.User).delete()
        db.commit()

def init_db(db: Session) -> None:
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
