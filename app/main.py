import logging

from typing import Optional

from fastapi import FastAPI


logger = logging.getLogger('app')

app = FastAPI(debug=True)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello")
async def hello():
    return {"message": "Hello 👋"}

@app.get("/hello/{name}")
async def hello_name(name: str, extra: Optional[str] = None):
    if extra is None:
        return {"message": f"Hello {name} 👋"}
    return {"message": f"Hello {name} 👋 {extra} 😎"}

@app.get("/test")
async def test():
    from pytube import YouTube
    yt = YouTube('http://youtube.com/watch?v=2lAe1cqCOXo')
    streams = yt.streams
    mp4_streams = streams.filter(only_video=True, file_extension='mp4')
    for streams in mp4_streams:
        logger.info(f"Video itag : {streams.itag} Resolution : {streams.resolution} VCodec : {streams.codecs[0]}")
    video = mp4_streams.first()
    fname = video.download('../downloads/', filename_prefix=f"[{yt.video_id}] ")
    return {
        "message": "Download finished",
        "fname": fname
        }
