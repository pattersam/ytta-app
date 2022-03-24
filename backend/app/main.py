from fastapi import FastAPI, Request, Depends, APIRouter
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import sqlalchemy.exc
import pytube.exceptions

from app.api.api_v1.api import api_router
from app.core.config import settings

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

index_api_router = APIRouter()

@index_api_router.get("/")
def index():
    return {"message": "Welcome to the YTTA API 👋"}

@app.exception_handler(sqlalchemy.exc.IntegrityError)
async def integrety_error_exception_handler(request: Request, exc: sqlalchemy.exc.IntegrityError):
    logger.error(exc)
    return JSONResponse(
        status_code=409,
        content={"message": f"Database integrity error..."},
    )

@app.exception_handler(pytube.exceptions.RegexMatchError)
async def pytube_regex_exception_handler(request: Request, exc: pytube.exceptions.RegexMatchError):
    logger.error(exc)
    return JSONResponse(
        status_code=406,
        content={"message": f"Unable to read URL..."},
    )

@app.exception_handler(pytube.exceptions.VideoUnavailable)
async def pytube_video_unavailable_exception_handler(request: Request, exc: pytube.exceptions.RegexMatchError):
    logger.error(exc)
    return JSONResponse(
        status_code=415,
        content={"message": f"Video unavailable..."},
    )

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

async def log_request_info(request: Request):
    logger.info(
        f"{request.method} request to {request.url} metadata\n"
        f"\tHeaders: {request.headers}\n"
        f"\tBody: {await request.body()}\n"
        f"\tPath Params: {request.path_params}\n"
        f"\tQuery Params: {request.query_params}\n"
        f"\tCookies: {request.cookies}\n"
    )

app.include_router(
    api_router,
    prefix=settings.API_V1_STR,
    dependencies=[Depends(log_request_info)],
    )

app.include_router(
    index_api_router,
    dependencies=[Depends(log_request_info)],
    )
