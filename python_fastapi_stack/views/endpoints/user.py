from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from python_fastapi_stack import crud, models
from python_fastapi_stack.paths import TEMPLATES_PATH
from python_fastapi_stack.views import deps

router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_PATH)


@router.get("/{username}", response_class=HTMLResponse)
async def view_user(
    request: Request,
    username: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
) -> Response:
    """
    Display a users account page.

    Args:
        request(Request): The request object
        username(str): The username to view
        current_user(models.User): The current user
        db(Session): The database session.

    Returns:
        Response: The users account page
    """
    db_user = await crud.user.get(db=db, username=username)
    context = {"request": request, "current_user": current_user, "db_user": db_user}
    return templates.TemplateResponse("user/view.html", context=context)


@router.get("/{username}/edit", response_class=HTMLResponse)
async def edit_user_account(
    request: Request,
    username: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
) -> Response:
    """
    Display the users account edit page.

    Args:
        request(Request): The request object
        username(str): The username to view
        current_user(models.User): The current user
        db(Session): The database session.

    Returns:
        Response: The users account page
    """
    db_user = await crud.user.get(db=db, username=username)
    context = {"request": request, "current_user": current_user, "db_user": db_user}
    return templates.TemplateResponse("user/edit.html", context=context)


@router.post("/{username}/edit", response_class=HTMLResponse)
async def update_user_account(
    request: Request,
    username: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
    full_name: str = Form(...),
    email: str = Form(...),
    is_active: bool = Form(False),
    is_superuser: bool = Form(False),
) -> Response:
    """
    Update the users account.

    Args:
        request(Request): The request object
        username(str): The username to view
        db(Session): The database session.
        current_user(models.User): The current user
        full_name(str): The users full name
        email(str): The users email
        is_active(bool): Is the user active
        is_superuser(bool): Is the user a superuser

    Returns:
        Response: The users account page
    """
    db_user = await crud.user.get(db=db, username=username)

    if current_user.is_superuser:
        user_update = models.UserUpdate(
            full_name=full_name, email=email, is_active=is_active, is_superuser=is_superuser
        )
    else:
        user_update = models.UserUpdate(full_name=full_name, email=email)

    db_user = await crud.user.update(db=db, in_obj=user_update, id=db_user.id)

    context = {"request": request, "current_user": current_user, "db_user": db_user}
    return templates.TemplateResponse(
        "user/edit.html", context=context, status_code=status.HTTP_200_OK
    )
