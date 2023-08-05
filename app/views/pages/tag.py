from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from sqlmodel import Session

from app import crud, models
from app.views import deps, templates

router = APIRouter()


@router.get("/tags", response_class=HTMLResponse)
async def list_tags(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Returns HTML response with list of tags.

    Args:
        request(Request): The request object
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: HTML page with the tags

    """
    # Get alerts dict from cookies
    alerts = models.Alerts().from_cookies(request.cookies)

    tags = await crud.tag.get_all(db=db)
    tags.sort(key=lambda x: x.name)

    return templates.TemplateResponse(
        "tag/list.html",
        {"request": request, "tags": tags, "current_user": current_user, "alerts": alerts},
    )


@router.get("/tags/all", response_class=HTMLResponse)
async def list_all_tags(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_superuser
    ),
) -> Response:
    """
    Returns HTML response with list of all tags from all users.

    Args:
        request(Request): The request object
        db(Session): The database session.
        current_user(User): The authenticated superuser.

    Returns:
        Response: HTML page with the tags

    """
    # Get alerts dict from cookies
    alerts = models.Alerts().from_cookies(request.cookies)

    tags = await crud.tag.get_all(db=db)
    tags.sort(key=lambda x: x.name)

    return templates.TemplateResponse(
        "tag/list.html",
        {"request": request, "tags": tags, "current_user": current_user, "alerts": alerts},
    )


@router.get("/tag/create", response_class=HTMLResponse)
async def create_tag(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    New Tag form.

    Args:
        request(Request): The request object
        current_user(User): The authenticated user.

    Returns:
        Response: Form to create a new tag
    """
    alerts = models.Alerts().from_cookies(request.cookies)

    options_channels = await crud.channel.get_all(db=db)
    options_channels.sort(key=lambda x: x.name)

    return templates.TemplateResponse(
        "tag/create.html",
        {
            "request": request,
            "options_channels": options_channels,
            "current_user": current_user,
            "alerts": alerts,
        },
    )


@router.post("/tag/create", response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
async def handle_create_tag(
    name: str = Form(...),
    channels: list[str] = Form(None),
    color: str = Form(None),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Handles the creation of a new tag.

    Args:
        name(str): The name of the tag
        channels(list[str]): List of selected channel ids
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: List of tags view
    """
    alerts = models.Alerts()
    tag_create = models.TagCreate(name=name, color=color)
    try:
        db_tag = await crud.tag.create(db=db, obj_in=tag_create)
    except crud.RecordAlreadyExistsError:
        alerts.danger.append("Tag already exists")
        response = RedirectResponse("/tags/create", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    # Update Channel Tags
    if channels:
        db_tag = await crud.channel.update_tag_of_channels(
            db=db, tag_id=db_tag.id, channel_ids=channels
        )

    alerts.success.append(f"Tag '{db_tag.name}' successfully created")
    response = RedirectResponse(url="/tags", status_code=status.HTTP_303_SEE_OTHER)
    response.headers["Method"] = "GET"
    response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
    return response


@router.get("/tag/{tag_id}", response_class=HTMLResponse)
async def view_tag(
    request: Request,
    tag_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    View tag.

    Args:
        request(Request): The request object
        tag_id(str): The tag id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: View of the tag
    """
    alerts = models.Alerts()
    try:
        tag = await crud.tag.get(db=db, id=tag_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Tag not found")
        response = RedirectResponse("/tags", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    tags = await crud.tag.get_all(db=db)
    tags.sort(key=lambda x: x.name)

    tag_channels = tag.channels
    tag_channels.sort(key=lambda x: x.name)

    return templates.TemplateResponse(
        "tag/view.html",
        {
            "request": request,
            "tag": tag,
            "tag_channels": tag_channels,
            "tags": tags,
            "current_user": current_user,
            "alerts": alerts,
        },
    )


@router.get("/tag/{tag_id}/edit", response_class=HTMLResponse)
async def edit_tag(
    request: Request,
    tag_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    New Tag form.

    Args:
        request(Request): The request object
        tag_id(str): The tag id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: Form to create a new tag
    """
    alerts = models.Alerts().from_cookies(request.cookies)
    try:
        tag = await crud.tag.get(db=db, id=tag_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Tag not found")
        response = RedirectResponse("/tags", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    options_channels = await crud.channel.get_all(db=db)
    options_channels.sort(key=lambda x: x.name)

    return templates.TemplateResponse(
        "tag/edit.html",
        {
            "request": request,
            "tag": tag,
            "options_channels": options_channels,
            "current_user": current_user,
            "alerts": alerts,
        },
    )


@router.post("/tag/{tag_id}/edit", response_class=HTMLResponse)
async def handle_edit_tag(
    request: Request,
    tag_id: str,
    name: str = Form(...),
    color: str = Form(...),
    channels: list[str] = Form(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Handles the creation of a new tag.

    Args:
        request(Request): The request object
        tag_id(str): The tag id
        name(str): The name of the tag
        channels(list[str]): List of selected channel ids
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: View of the newly created tag
    """
    alerts = models.Alerts()
    tag_update = models.TagUpdate(name=name, color=color)

    # Update Tag Details
    try:
        db_tag = await crud.tag.update(db=db, obj_in=tag_update, id=tag_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Tag not found")
        response = RedirectResponse(url="/tags", status_code=status.HTTP_303_SEE_OTHER)
        response.headers["Method"] = "GET"
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    # Update Channel Tags
    db_tag = await crud.channel.update_tag_of_channels(db=db, tag_id=tag_id, channel_ids=channels)

    alerts.success.append(f"Tag '{db_tag.name}' updated")

    response = RedirectResponse(f"/tag/{tag_id}/edit", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
    return response


@router.get("/tag/{tag_id}/delete", response_class=HTMLResponse)
async def delete_tag(
    tag_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    New Tag form.

    Args:
        tag_id(str): The tag id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: Form to create a new tag
    """
    alerts = models.Alerts()
    try:
        await crud.tag.remove(db=db, id=tag_id)
        alerts.success.append("Tag deleted")
    except crud.RecordNotFoundError:
        alerts.danger.append("Tag not found")
    except crud.DeleteError:
        alerts.danger.append("Error deleting tag")

    response = RedirectResponse(url="/tags", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="alerts", value=alerts.json(), max_age=5, httponly=True)
    return response
