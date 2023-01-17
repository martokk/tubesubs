from fastapi import APIRouter, Depends, HTTPException, Request, status
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

    Raises:
        HTTPException: User not found
    """
    try:
        videos = await crud.video.get_all(db=db)
    except crud.RecordNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Videos not found",
        ) from e
    # sources = await source_crud.get_many(created_by=user.id)
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
