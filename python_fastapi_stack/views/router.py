from fastapi import APIRouter

from python_fastapi_stack.views.endpoints import videos

views_router = APIRouter()
views_router.include_router(videos.router, tags=["Views"])
