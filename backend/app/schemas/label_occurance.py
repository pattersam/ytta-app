from typing import Optional

from pydantic import BaseModel


# Shared properties
class LabelOccuranceBase(BaseModel):
    num_occurances: Optional[int] = None
    avg_confidence: Optional[float] = None


# Properties to receive on video creation
class LabelOccuranceCreate(LabelOccuranceBase):
    pass


# Properties to receive on video update
class LabelOccuranceUpdate(LabelOccuranceBase):
    pass


# Properties shared by models stored in DB
class LabelOccuranceInDBBase(LabelOccuranceBase):
    id: int
    num_occurances: int
    avg_confidence: float
    video_id: int
    label_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class LabelOccurance(LabelOccuranceInDBBase):
    pass


# Properties properties stored in DB
class LabelOccuranceInDB(LabelOccuranceInDBBase):
    pass
