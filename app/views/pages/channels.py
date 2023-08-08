from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from sqlmodel import Session

from app import crud, models
from app.views import deps, templates

router = APIRouter()


@router.get("/channels", response_class=HTMLResponse)
@router.get("/channels/hidden", response_class=HTMLResponse)
async def list_channels(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Response:
    """
    Returns HTML response with list of channels.

    Args:
        request(Request): The request object
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: HTML page with the channels

    """
    # Get alerts dict from cookies
    alerts = models.Alerts().from_cookies(request.cookies)

    if "/channels/hidden" in request.url.path:
        title = "Hidden Channels"
        is_hidden = True
        action = "unhide"
    else:
        title = "Visible Channels"
        is_hidden = False
        action = "hide"

    subscribed_channels = await crud.channel.get_multi(
        db=db, is_hidden=is_hidden, is_subscribed=True
    )
    subscribed_channels.sort(key=lambda x: x.name)

    not_subscribed_channels = await crud.channel.get_multi(
        db=db, is_hidden=is_hidden, is_subscribed=False
    )
    not_subscribed_channels.sort(key=lambda x: x.name)

    tags = await crud.tag.get_all(db=db)
    tags.sort(key=lambda x: x.name)

    return templates.TemplateResponse(
        "channel/list.html",
        {
            "request": request,
            "title": title,
            "subscribed_channels": subscribed_channels,
            "not_subscribed_channels": not_subscribed_channels,
            "tags": tags,
            "current_user": current_user,
            "alerts": alerts,
            "action": action,  # Pass the action variable to the template
        },
    )


@router.get("/channel/{channel_id}/hide", response_class=HTMLResponse)
async def handle_hide_channel(
    channel_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Handle Hide Channel

    Args:
        channel_id(str): The channel id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Redirect to /channels after hiding the channel
    """
    alerts = models.Alerts()
    try:
        channel = await crud.channel.get(db=db, id=channel_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Channel not found")
        response = RedirectResponse("/channels", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    channel_update = models.ChannelUpdate(is_hidden=True)
    await crud.channel.update(db=db, id=channel.id, obj_in=channel_update)

    alerts.success.append(f"Channel '{channel.name}' was hidden.")

    response = RedirectResponse(url="/channels", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="alerts", value=alerts.json(), max_age=5, httponly=True)
    return response


@router.get("/channel/{channel_id}/unhide", response_class=HTMLResponse)
async def handle_unhide_channel(
    channel_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Handle Unhide Channel

    Args:
        channel_id(str): The channel id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Redirect to /channels after hiding the channel
    """
    alerts = models.Alerts()
    try:
        channel = await crud.channel.get(db=db, id=channel_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Channel not found")
        response = RedirectResponse("/channels", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    channel_update = models.ChannelUpdate(is_hidden=False)
    await crud.channel.update(db=db, id=channel.id, obj_in=channel_update)

    alerts.success.append(f"Channel '{channel.name}' was unhidden.")

    response = RedirectResponse(url="/channels", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="alerts", value=alerts.json(), max_age=5, httponly=True)
    return response


@router.get("/channel/{channel_id}", response_class=HTMLResponse)
async def view_channel(
    request: Request,
    channel_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    View channel.

    Args:
        request(Request): The request object
        channel_id(str): The channel id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: View of the channel
    """
    alerts = models.Alerts().from_cookies(request.cookies)
    try:
        db_channel = await crud.channel.get(db=db, id=channel_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Channel not found")
        response = RedirectResponse("/channels", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    return templates.TemplateResponse(
        "channel/view.html",
        {
            "request": request,
            "channel": db_channel,
            "current_user": current_user,
            "alerts": alerts,
        },
    )


@router.get("/channel/{channel_id}/edit", response_class=HTMLResponse)
async def edit_channel(
    request: Request,
    channel_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Edit channel form.

    Args:
        request(Request): The request object
        channel_id(str): The channel id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: Form to edit a channel
    """
    alerts = models.Alerts().from_cookies(request.cookies)
    try:
        db_channel = await crud.channel.get(db=db, id=channel_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Channel not found")
        response = RedirectResponse("/channels", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    options_tags = await crud.tag.get_all(db=db)
    options_tags.sort(key=lambda x: x.name)

    return templates.TemplateResponse(
        "channel/edit.html",
        {
            "request": request,
            "channel": db_channel,
            "options_tags": options_tags,
            "current_user": current_user,
            "alerts": alerts,
        },
    )


@router.post("/channel/{channel_id}/edit", response_class=HTMLResponse)
async def handle_edit_channel(
    request: Request,
    channel_id: str,
    is_hidden: bool = Form(False),
    tags: list[str] = Form(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Handles the edit of a channel.

    Args:
        request(Request): The request object
        channel_id(str): The channel id
        tags(list[str]): List of selected tags
        is_hidden(bool):
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: View of the edited channel
    """
    alerts = models.Alerts()
    channel_update = models.ChannelUpdate(
        is_hidden=is_hidden,
    )

    # Update Channel Details
    try:
        db_channel = await crud.channel.update(db=db, obj_in=channel_update, id=channel_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Channel not found")
        response = RedirectResponse(url="/channels", status_code=status.HTTP_303_SEE_OTHER)
        response.headers["Method"] = "GET"
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    # Update Channel Tags
    db_channel = await crud.channel.update_tags(db=db, channel_id=channel_id, tag_ids=tags)

    alerts.success.append(f"Channel '{db_channel.name}' updated")

    response = RedirectResponse(
        f"/channel/{channel_id}/edit", status_code=status.HTTP_303_SEE_OTHER
    )
    response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
    return response
