from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.schemas.label_occurance import LabelOccuranceCreate, LabelOccuranceUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.label import create_random_label
from app.tests.utils.video import create_random_video
from app.tests.utils.label_occurance import create_random_label_occurance
from app.tests.utils.utils import random_lower_string


def test_create_label_occurance(db: Session) -> None:
    num_occurances = 1
    avg_confidence = 10.0
    label_occurance_in = LabelOccuranceCreate(
        num_occurances=num_occurances,
        avg_confidence=avg_confidence,
    )
    label = create_random_label(db)
    video = create_random_video(db)
    label_occurance = crud.label_occurance.create(
        db, obj_in=label_occurance_in, label_id=label.id, video_id=video.id
    )
    assert label_occurance.num_occurances == num_occurances
    assert label_occurance.avg_confidence == avg_confidence
    assert label_occurance.label_id == label.id
    assert label_occurance.video_id == video.id


def test_get_label_occurance(db: Session) -> None:
    num_occurances = 2
    avg_confidence = 30.0
    label_occurance_in = LabelOccuranceCreate(
        num_occurances=num_occurances,
        avg_confidence=avg_confidence,
    )
    label = create_random_label(db)
    video = create_random_video(db)
    label_occurance = crud.label_occurance.create(
        db, obj_in=label_occurance_in, label_id=label.id, video_id=video.id
    )
    label_occurance_2 = crud.label_occurance.get(db, id=label_occurance.id)
    assert label_occurance_2
    assert label_occurance.num_occurances == label_occurance_2.num_occurances
    assert label_occurance.avg_confidence == label_occurance_2.avg_confidence
    assert label_occurance.label_id == label_occurance_2.label_id
    assert label_occurance.video_id == label_occurance_2.video_id
    assert jsonable_encoder(label_occurance) == jsonable_encoder(label_occurance_2)


def test_get_label_occurance_by_owner(db: Session) -> None:
    owner = create_random_user(db)
    video = create_random_video(db, owner_id=owner.id)
    l1 = create_random_label(db)
    l2 = create_random_label(db)
    lo_in1 = LabelOccuranceCreate(num_occurances=3, avg_confidence=30)
    lo_in2 = LabelOccuranceCreate(num_occurances=40, avg_confidence=40)
    lo1 = crud.label_occurance.create(db, obj_in=lo_in1, label_id=l1.id, video_id=video.id)
    lo2 = crud.label_occurance.create(db, obj_in=lo_in2, label_id=l2.id, video_id=video.id)
    label_occurances = crud.label_occurance.get_multi_by_owner(db, owner_id=owner.id)
    assert label_occurances
    assert len(label_occurances) == 2
    assert jsonable_encoder(label_occurances) == jsonable_encoder([lo1, lo2])


def test_update_label_occurance(db: Session) -> None:
    num_occurances = 5
    avg_confidence = 50.0
    label_occurance_in = LabelOccuranceCreate(
        num_occurances=num_occurances,
        avg_confidence=avg_confidence,
    )
    label = create_random_label(db)
    video = create_random_video(db)
    label_occurance = crud.label_occurance.create(
        db, obj_in=label_occurance_in, label_id=label.id, video_id=video.id
    )
    new_num_occurances = num_occurances + 1
    label_occurance_in_update = LabelOccuranceUpdate(num_occurances=new_num_occurances)
    crud.label_occurance.update(
        db, db_obj=label_occurance, obj_in=label_occurance_in_update
    )
    label_occurance_2 = crud.label_occurance.get(db, id=label_occurance.id)
    assert label_occurance_2
    assert label_occurance.num_occurances == label_occurance_2.num_occurances


def test_update_label_occurance_from_dict(db: Session) -> None:
    num_occurances = 6
    avg_confidence = 60.0
    label_occurance_in = LabelOccuranceCreate(
        num_occurances=num_occurances,
        avg_confidence=avg_confidence,
    )
    label = create_random_label(db)
    video = create_random_video(db)
    label_occurance = crud.label_occurance.create(
        db, obj_in=label_occurance_in, label_id=label.id, video_id=video.id
    )
    new_num_occurances = num_occurances + 1
    crud.label_occurance.update(
        db, db_obj=label_occurance, obj_in={"num_occurances": new_num_occurances}
    )
    label_occurance_2 = crud.label_occurance.get(db, id=label_occurance.id)
    assert label_occurance_2
    assert label_occurance.num_occurances == label_occurance_2.num_occurances
