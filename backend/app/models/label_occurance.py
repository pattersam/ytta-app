from typing import TYPE_CHECKING

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Float,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class LabelOccurance(Base):
    id = Column(Integer, primary_key=True, index=True)
    num_occurances = Column(Integer)
    avg_confidence = Column(Float)
    label_id = Column(Integer, ForeignKey("label.id"))
    label = relationship("Label", back_populates="occurances")
    video_id = Column(Integer, ForeignKey("video.id"))
    video = relationship("Video", back_populates="label_occurances")

    __table_args__ = (UniqueConstraint("video_id", "label_id", name="_video_label_uc"),)
