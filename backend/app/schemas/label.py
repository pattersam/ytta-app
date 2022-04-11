from typing import Optional

from pydantic import BaseModel


# Shared properties
class LabelBase(BaseModel):
    name: Optional[str] = None


# Properties to receive via API on creation
class LabelCreate(LabelBase):
    pass


# Properties to receive via API on update
class LabelUpdate(LabelBase):
    pass


class LabelInDBBase(LabelBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Label(LabelInDBBase):
    pass


# Additional properties stored in DB
class LabelInDB(LabelInDBBase):
    pass
