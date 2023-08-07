from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session

from app import crud, models
from app.views import deps

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root_index_router(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    """
    Home page router

    Args:
        request(Request): The request object
        current_user(models.User): The current user

    Returns:
        Response: Home page
    """
    if current_user:
        return await root_index_authenticated(request=request, db=db, current_user=current_user)
    return await root_index_unauthenticated()


async def root_index_unauthenticated() -> Response:
    """
    Home page (Not authenticated)

    Returns:
        Response: Home page
    """
    return RedirectResponse(url="/login")


async def root_index_authenticated(
    request: Request,
    db: Session,
    current_user: models.User,
) -> Response:
    """
    Home page. (Authenticated)

    Args:
        request(Request): The request object
        current_user(models.User): The current user

    Returns:
        Response: Home page
    """
    default_filter_group_name = "All Unread"
    try:
        default_filter_group = await crud.filter_group.get(db=db, name=default_filter_group_name)
    except crud.RecordNotFoundError:
        return RedirectResponse(url="/filter-groups")
    return RedirectResponse(url=f"/filter-group/{default_filter_group.id}")
