from fastapi import APIRouter

from app.views.pages import (
    account,
    channels,
    filters,
    login,
    playlist,
    playlist_item,
    root,
    subscriptions,
    tag,
    user,
    videos,
)

views_router = APIRouter(include_in_schema=False)
views_router.include_router(root.router, tags=["Views"])
views_router.include_router(videos.router, tags=["Videos"])
views_router.include_router(subscriptions.router, tags=["Subscriptions"])
views_router.include_router(filters.router, tags=["Filters"])
views_router.include_router(playlist.router, tags=["Playlists"])
views_router.include_router(playlist_item.router, tags=["Playlist Items"])
views_router.include_router(channels.router, tags=["Channels"])
views_router.include_router(tag.router, tags=["Tags"])
views_router.include_router(login.router, tags=["Logins"])
views_router.include_router(account.router, prefix="/account", tags=["Account"])
views_router.include_router(user.router, prefix="/user", tags=["Users"])
