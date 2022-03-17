import logging

from typing import Optional

from fastapi import FastAPI, Query
from pytube import YouTube


logger = logging.getLogger('api')


description = """
Build a picture of your YouTube usage 📺
"""

tags_metadata = [
    {
        "name": "videos",
        "description": "Operations with videos.",
    },
]

app = FastAPI(
    title="YouTube Tag Analysis API",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata,
    debug=True,
    )


@app.get("/")
def root():
    return {"msg": "YouTube Tag Analyser API"}

@app.get("/videos/", tags=["videos"])
def get_videos():
    return {"msg": "TO BE IMPLEMENTED"}

@app.get("/videos/{video_id}", tags=["videos"])
def get_video(video_id: str):
    return {"msg": f"TO BE IMPLEMENTED {video_id}"}

@app.post("/videos/", tags=["videos"])
def post_video(
    url: str = Query(
        ...,
        description='URL of a YouTube video',
        example='https://www.youtube.com/watch?v=ykwyamBDUu8'
        )
    ):
    logger.info(f"Downloading: {url}")
    yt = YouTube(url)
    fname = yt.streams.filter(only_video=True, file_extension='mp4').first().download('downloads/', filename_prefix=f"[{yt.video_id}] ")
    return {
        "msg": "Download finished",
        "fname": fname,
        }
