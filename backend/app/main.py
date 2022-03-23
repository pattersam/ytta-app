from fastapi import FastAPI, Request
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

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
