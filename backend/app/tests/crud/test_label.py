from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.schemas.label import LabelCreate, LabelUpdate
from app.tests.utils.utils import random_lower_string


def test_create_label(db: Session) -> None:
    name = random_lower_string()
    label_in = LabelCreate(name=name)
    label = crud.label.create(db, obj_in=label_in)
    assert label.name == name


def test_get_label(db: Session) -> None:
    name = random_lower_string()
    label_in = LabelCreate(name=name)
    label = crud.label.create(db, obj_in=label_in)
    label_2 = crud.label.get(db, id=label.id)
    assert label_2
    assert label.name == label_2.name
    assert jsonable_encoder(label) == jsonable_encoder(label_2)


def test_update_label(db: Session) -> None:
    name = random_lower_string()
    label_in = LabelCreate(name=name)
    label = crud.label.create(db, obj_in=label_in)
    new_name = random_lower_string()
    label_in_update = LabelUpdate(name=new_name)
    crud.label.update(db, db_obj=label, obj_in=label_in_update)
    label_2 = crud.label.get(db, id=label.id)
    assert label_2
    assert label.name == label_2.name


def test_update_label_from_dict(db: Session) -> None:
    name = random_lower_string()
    label_in = LabelCreate(name=name)
    label = crud.label.create(db, obj_in=label_in)
    new_name = random_lower_string()
    crud.label.update(db, db_obj=label, obj_in={"name": new_name})
    label_2 = crud.label.get(db, id=label.id)
    assert label_2
    assert label.name == label_2.name
