from typing import Optional

from fastapi import FastAPI

app = FastAPI()


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
