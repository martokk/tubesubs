from fastapi import APIRouter

from python_fastapi_stack.views.endpoints import items, login, root

views_router = APIRouter(include_in_schema=False)
views_router.include_router(root.router, tags=["Views"])
views_router.include_router(items.router, tags=["Items"])
views_router.include_router(login.router, tags=["Logins"])
