import logging

from typing import Optional

from fastapi import FastAPI
from pytube import YouTube


logger = logging.getLogger('api')

app = FastAPI(debug=True)


@app.get("/")
async def root():
    return {"msg": "YouTube Tag Analyser API"}

@app.get("/hello")
async def hello():
    return {"msg": "Hello 👋"}

@app.get("/hello/{name}")
async def hello_name(name: str, extra: Optional[str] = None):
    if extra is None:
        return {"msg": f"Hello {name} 👋"}
    return {"msg": f"Hello {name} 👋 {extra} 😎"}

@app.get("/yt")
async def yt(url: Optional[str] = None):
    if url is None:
        return {"msg": "Please give a youtube video url query parameter, e.g. ?url=https://www.youtube.com/watch?v=ykwyamBDUu8"}
    logger.info(f"Downloading: {url}")
    yt = YouTube(url)
    video = yt.streams.filter(only_video=True, file_extension='mp4').first()
    fname = video.download('../downloads/', filename_prefix=f"[{yt.video_id}] ")
    return {
        "msg": "Download finished",
        "fname": fname,
        }
