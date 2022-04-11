from fastapi import APIRouter

from app.api.api_v1.endpoints import videos, labels, label_occurances, login, users, utils

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(labels.router, prefix="/labels", tags=["labels"])
api_router.include_router(label_occurances.router, prefix="/label_occurances", tags=["label_occurances"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(videos.router, prefix="/videos", tags=["videos"])
