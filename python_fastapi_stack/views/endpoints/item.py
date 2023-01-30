from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from python_fastapi_stack import crud
from python_fastapi_stack.api.deps import get_db

router = APIRouter()
templates = Jinja2Templates(directory="python_fastapi_stack/views/templates")


@router.get("/items", summary="Returns HTML Response with the item", response_class=HTMLResponse)
async def html_view_items(request: Request, db: Session = Depends(get_db)) -> Response:
    """
    Returns HTML response with list of items.

    Args:
        request(Request): The request object
        db(Session): The database session.

    Returns:
        Response: HTML page with the items

    """
    items = await crud.item.get_all(db=db)
    items_context = [
        {
            "id": item.id,
            "title": item.title,
            "url": item.url,
        }
        for item in items
    ]
    context = {"request": request, "items": items_context}
    return templates.TemplateResponse("view_items.html", context)
