from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from python_fastapi_stack import crud
from python_fastapi_stack.api.deps import get_db

router = APIRouter()
templates = Jinja2Templates(directory="python_fastapi_stack/views/templates")


@router.get("/videos", summary="Returns HTML Response with the video", response_class=HTMLResponse)
async def html_view_videos(request: Request, db: Session = Depends(get_db)) -> Response:
    """
    Returns HTML response with list of videos.

    Args:
        request(Request): The request object
        db(Session): The database session.

    Returns:
        Response: HTML page with the videos

    """
    videos = await crud.video.get_all(db=db)
    videos_context = [
        {
            "id": video.id,
            "title": video.title,
            "url": video.url,
        }
        for video in videos
    ]
    context = {"request": request, "videos": videos_context}
    return templates.TemplateResponse("view_videos.html", context)
