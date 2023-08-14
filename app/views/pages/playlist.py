from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from sqlmodel import Session

from app import crud, logger, models
from app.services.feed import build_rss_file, get_rss_file
from app.views import deps, templates

router = APIRouter()


@router.get("/playlists", response_class=HTMLResponse)
async def list_playlists(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Returns HTML response with list of playlists.

    Args:
        request(Request): The request object
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: HTML page with the playlists

    """
    # Get alerts dict from cookies
    alerts = models.Alerts().from_cookies(request.cookies)

    playlists = await crud.playlist.get_all(db=db)
    playlists.sort(key=lambda x: x.name)

    return templates.TemplateResponse(
        "playlist/list.html",
        {
            "request": request,
            "playlists": playlists,
            "current_user": current_user,
            "alerts": alerts,
        },
    )


@router.get("/playlists/all", response_class=HTMLResponse)
async def list_all_playlists(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_superuser
    ),
) -> Response:
    """
    Returns HTML response with list of all playlists from all users.

    Args:
        request(Request): The request object
        db(Session): The database session.
        current_user(User): The authenticated superuser.

    Returns:
        Response: HTML page with the playlists

    """
    # Get alerts dict from cookies
    alerts = models.Alerts().from_cookies(request.cookies)

    playlists = await crud.playlist.get_all(db=db)
    return templates.TemplateResponse(
        "playlist/list.html",
        {
            "request": request,
            "playlists": playlists,
            "current_user": current_user,
            "alerts": alerts,
        },
    )


@router.get("/playlist/create", response_class=HTMLResponse)
async def create_playlist(
    request: Request,
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    New Playlist form.

    Args:
        request(Request): The request object
        current_user(User): The authenticated user.

    Returns:
        Response: Form to create a new playlist
    """
    alerts = models.Alerts().from_cookies(request.cookies)

    return templates.TemplateResponse(
        "playlist/create.html",
        {
            "request": request,
            "current_user": current_user,
            "alerts": alerts,
        },
    )


@router.post("/playlist/create", response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
async def handle_create_playlist(
    name: str = Form(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Handles the creation of a new playlist.

    Args:
        name(str): The playlist name
        playlist_handler(str): The playlist_handler of the playlist
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: List of playlists view
    """
    alerts = models.Alerts()

    try:
        playlist_create = models.PlaylistCreate(
            name=name,
        )
    except ValueError as e:
        alerts.danger.append(e.args[0][0].exc.args[0])
        response = RedirectResponse("/playlist/create", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    try:
        await crud.playlist.create(db=db, obj_in=playlist_create)
    except crud.RecordAlreadyExistsError:
        alerts.danger.append("Playlist already exists")
        response = RedirectResponse("/playlist/create", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    alerts.success.append("Playlist successfully created")
    response = RedirectResponse(url="/playlists", status_code=status.HTTP_303_SEE_OTHER)
    response.headers["Method"] = "GET"
    response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
    return response


@router.get("/playlist/{playlist_id}", response_class=HTMLResponse)
async def view_playlist(
    request: Request,
    playlist_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    View playlist.

    Args:
        request(Request): The request object
        playlist_id(str): The playlist id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: View of the playlist
    """
    alerts = models.Alerts()
    try:
        playlist = await crud.playlist.get(db=db, id=playlist_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Playlist not found")
        response = RedirectResponse("/playlists", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    playlists = await crud.playlist.get_all(db=db)
    playlists.sort(key=lambda x: x.name)

    return templates.TemplateResponse(
        "playlist/view.html",
        {
            "request": request,
            "playlist": playlist,
            "playlists": playlists,
            "current_user": current_user,
            "alerts": alerts,
        },
    )


@router.get("/playlist/{playlist_id}/edit", response_class=HTMLResponse)
async def edit_playlist(
    request: Request,
    playlist_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Edit playlist form.

    Args:
        request(Request): The request object
        playlist_id(str): The playlist id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: Form to edit a playlist
    """
    alerts = models.Alerts().from_cookies(request.cookies)
    try:
        playlist = await crud.playlist.get(db=db, id=playlist_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Playlist not found")
        response = RedirectResponse("/playlists", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response
    return templates.TemplateResponse(
        "playlist/edit.html",
        {
            "request": request,
            "playlist": playlist,
            "current_user": current_user,
            "alerts": alerts,
        },
    )


@router.post("/playlist/{playlist_id}/edit", response_class=HTMLResponse)
async def handle_edit_playlist(
    request: Request,
    playlist_id: str,
    name: str = Form(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Handles the edit of a playlist.

    Args:
        request(Request): The request object
        playlist_id(str): The playlist id
        name(str): The service_handler of the playlist
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: View of the edited playlist
    """
    alerts = models.Alerts()
    playlist_update = models.PlaylistUpdate(
        name=name,
    )

    try:
        new_playlist = await crud.playlist.update(db=db, obj_in=playlist_update, id=playlist_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Playlist not found")
        response = RedirectResponse(url="/playlists", status_code=status.HTTP_303_SEE_OTHER)
        response.headers["Method"] = "GET"
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response
    alerts.success.append("Playlist updated")
    return templates.TemplateResponse(
        "playlist/edit.html",
        {
            "request": request,
            "playlist": new_playlist,
            "current_user": current_user,
            "alerts": alerts,
        },
    )


@router.get("/playlist/{playlist_id}/delete", response_class=HTMLResponse)
async def delete_playlist(
    playlist_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Delete Playlist view.

    Args:
        playlist_id(str): The playlist id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: Form to delete a new playlist
    """
    alerts = models.Alerts()
    try:
        await crud.playlist.remove(db=db, id=playlist_id)
        alerts.success.append("Playlist deleted")
    except crud.RecordNotFoundError:
        alerts.danger.append("Playlist not found")
    except crud.DeleteError:
        alerts.danger.append("Error deleting playlist")

    response = RedirectResponse(url="/playlists", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="alerts", value=alerts.json(), max_age=5, httponly=True)
    return response


@router.get("/playlist/{playlist_id}/feed", response_class=HTMLResponse)
async def get_playlist_rss_feed(playlist_id: str, db: Session = Depends(deps.get_db)) -> Response:
    """
    Gets a rss file for playlist and returns it as a Response

    Args:
        playlist_id(str): The playlist_id of the playlist.

    Returns:
        Response: The rss file as a Response.

    Raises:
        HTTPException: If the rss file is not found.
    """
    playlist = await crud.playlist.get(id=playlist_id, db=db)
    await build_rss_file(playlist=playlist)
    try:
        rss_file = await get_rss_file(id=playlist_id)
    except FileNotFoundError as exc:
        err_msg = f"RSS file ({playlist.id}.rss) does not exist for playlist '{playlist_id=}'"
        logger.critical(err_msg)
        # await notify(telegram=True, email=False, text=err_msg)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err_msg) from exc

    # Serve RSS File as a Response
    content = rss_file.read_text()
    return Response(content)
