from fastapi import APIRouter

from python_fastapi_stack.views.endpoints import item

views_router = APIRouter()
views_router.include_router(item.router, tags=["Views"])
