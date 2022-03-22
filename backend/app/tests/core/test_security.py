from datetime import timedelta
from jose import jwt
from sqlalchemy.orm import Session
from time import time

from app.core.config import settings
from app.core.security import create_access_token


def test_create_access_token(db: Session) -> None:
    subject = 'subject'
    encoded_jwt = create_access_token(subject)
    decoded_jwt = jwt.decode(encoded_jwt, settings.SECRET_KEY)
    assert decoded_jwt
    assert decoded_jwt['sub'] == subject


def test_create_access_token_with_60_second_expiry(db: Session) -> None:
    subject = 'subject'
    encoded_jwt = create_access_token(subject, expires_delta=timedelta(seconds=60))
    decoded_jwt = jwt.decode(encoded_jwt, settings.SECRET_KEY)
    assert decoded_jwt
    assert decoded_jwt['sub'] == subject
    assert abs(time() + 60 - decoded_jwt['exp']) < 1  # within +/-1 second
