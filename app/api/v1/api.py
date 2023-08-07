from fastapi import APIRouter

from app import models, settings, version
from app.api.v1.endpoints import channel, login, playlist_item, users, video

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/user", tags=["Users"])
api_router.include_router(playlist_item.router, prefix="/playlist-item", tags=["PlaylistItem"])
api_router.include_router(channel.router, prefix="/channel", tags=["Channel"])
api_router.include_router(video.router, prefix="/video", tags=["Video"])


@api_router.get("/", response_model=models.HealthCheck, tags=["status"])
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        dict[str, str]: Health check response.
    """
    return {
        "name": settings.PROJECT_NAME,
        "version": version,
        "description": settings.PROJECT_DESCRIPTION,
    }
