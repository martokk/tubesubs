from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from sqlmodel import Session

from app import crud, models
from app.views import deps, templates

router = APIRouter()


@router.get("/channels", response_class=HTMLResponse)
async def list_channels(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
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

    visible_channels = await crud.channel.get_multi(db=db, is_hidden=False)
    visible_channels.sort(key=lambda x: x.name)

    hidden_channels = await crud.channel.get_multi(db=db, is_hidden=True)
    hidden_channels.sort(key=lambda x: x.name)

    return templates.TemplateResponse(
        "channel/list.html",
        {
            "request": request,
            "visible_channels": visible_channels,
            "hidden_channels": hidden_channels,
            "current_user": current_user,
            "alerts": alerts,
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
