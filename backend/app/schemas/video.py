from typing import Optional

from pydantic import BaseModel


# Shared properties
class VideoBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    yt_id: Optional[str] = None


# Properties to receive on video creation
class VideoCreate(VideoBase):
    url: str


# Properties to receive on video update
class VideoUpdate(VideoBase):
    pass


# Properties shared by models stored in DB
class VideoInDBBase(VideoBase):
    id: int
    title: str
    yt_id: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Video(VideoInDBBase):
    pass


# Properties properties stored in DB
class VideoInDB(VideoInDBBase):
    pass
