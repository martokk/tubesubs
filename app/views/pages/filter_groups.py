import json

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from sqlmodel import Session

from app import crud, models
from app.models.filtered_videos import FilteredVideos
from app.services.fetch import fetch_all_subscriptions, fetch_filter_group
from app.services.filter_videos import get_filtered_videos
from app.views import deps, templates

# from app.services.fetch import fetch_filter_group

router = APIRouter()


@router.get("/filter-groups", response_class=HTMLResponse)
async def list_filter_groups(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Returns HTML response with list of filter_groups.

    Args:
        request(Request): The request object
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: HTML page with the filter_groups

    """
    # Get alerts dict from cookies
    alerts = models.Alerts().from_cookies(request.cookies)

    # Get all filter_groups
    filter_groups = await crud.filter_group.get_all(db=db)
    filter_groups.sort(key=lambda x: x.name)

    # # Get unread count for each filter_group
    filter_group_unread_count = {}
    for filter_group_ in filter_groups:
        # filter_grouped_videos = await get_filter_grouped_videos(filter_group_=filter_group_)
        # filter_group_unread_count[filter_group_.id] = filter_grouped_videos.videos_not_limited_count
        filter_group_unread_count[filter_group_.id] = -1

    # # Separate pinned filter_groups
    # pinned_filter_group_names = ["All Unread", "Missing Tags"]
    # pinned_filter_groups = []
    # for filter_group_ in filter_groups:
    #     if filter_group_.name in pinned_filter_group_names:
    #         pinned_filter_groups.append(filter_group_)
    #         filter_groups.remove(filter_group_)

    return templates.TemplateResponse(
        "filter_group/list.html",
        {
            "request": request,
            # "pinned_filter_groups": pinned_filter_groups,
            "filter_groups": filter_groups,
            "filter_group_unread_count": filter_group_unread_count,
            "current_user": current_user,
            "alerts": alerts,
        },
    )


@router.get("/filter-group/create", response_class=HTMLResponse)
async def create_filter_group(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    New FilterGroup form.

    Args:
        request(Request): The request object
        current_user(User): The authenticated user.

    Returns:
        Response: Form to create a new filter_group
    """
    alerts = models.Alerts().from_cookies(request.cookies)

    options_filters = await crud.filter.get_all(db=db)
    options_filters.sort(key=lambda x: x.name)

    return templates.TemplateResponse(
        "filter_group/create.html",
        {
            "request": request,
            "current_user": current_user,
            "alerts": alerts,
            "options_filters": options_filters,
        },
    )


@router.post(
    "/filter-group/create", response_class=HTMLResponse, status_code=status.HTTP_201_CREATED
)
async def handle_create_filter_group(
    name: str = Form(...),
    filter_ids: list[str] = Form(...),
    ordered_filter_ids_str: str = Form(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Handles the creation of a new filter_group.

    Args:
        name(str): Name of the FilterGroup
        filters(list[str]): The filters
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: List of filter_groups view
    """
    alerts = models.Alerts()

    ordered_filter_ids = json.loads(ordered_filter_ids_str)

    filters = [await crud.filter.get(db=db, id=filter_id) for filter_id in ordered_filter_ids]

    # Create FilterGroup and Save in Database
    try:
        filter_group_create = models.FilterGroupCreate(
            name=name, ordered_filter_ids_str=ordered_filter_ids_str
        )
    except ValueError as e:
        alerts.danger.append(e.args[0][0].exc.args[0])
        response = RedirectResponse("/filter-group/create", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    try:
        db_filter_group = await crud.filter_group.create(db=db, obj_in=filter_group_create)
    except crud.RecordAlreadyExistsError:
        alerts.danger.append("FilterGroup already exists")
        response = RedirectResponse("/filter-group/create", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    # Add Filters
    db_filter_group.filters = filters
    db.commit()

    # Redirect on Success
    alerts.success.append("FilterGroup successfully created")
    response = RedirectResponse(
        url=f"/filter-group/{db_filter_group.id}", status_code=status.HTTP_303_SEE_OTHER
    )
    response.headers["Method"] = "GET"
    response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
    return response


@router.get("/filter-group/{filter_group_id}/edit", response_class=HTMLResponse)
async def edit_filter_group(
    request: Request,
    filter_group_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Edit filter_group form.

    Args:
        request(Request): The request object
        filter_group_id(str): The filter_group id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: Form to edit a filter_group
    """
    alerts = models.Alerts().from_cookies(request.cookies)
    try:
        db_filter_group = await crud.filter_group.get(db=db, id=filter_group_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("FilterGroup not found")
        response = RedirectResponse("/filter-groups", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    # Build FilterGroup Options
    options_filters = await crud.filter.get_all(db=db)
    options_filters.sort(key=lambda x: x.name)

    return templates.TemplateResponse(
        "filter_group/edit.html",
        {
            "request": request,
            "filter_group": db_filter_group,
            "current_user": current_user,
            "alerts": alerts,
            "options_filters": options_filters,
        },
    )


@router.post("/filter-group/{filter_group_id}/edit", response_class=HTMLResponse)
async def handle_edit_filter_group(
    request: Request,
    filter_group_id: str,
    name: str = Form(...),
    ordered_filter_ids_str: str = Form(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Handles the edit of a filter_group.

    Args:
        request(Request): The request object
        filter_group_id(str): The filter_group id
        service_handler(str): The service_handler of the filter_group
        filter_group_handler(str): The filter_group_handler of the filter_group
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: View of the edited filter_group
    """
    alerts = models.Alerts()

    ordered_filter_ids = json.loads(ordered_filter_ids_str)

    filters = [await crud.filter.get(db=db, id=filter_id) for filter_id in ordered_filter_ids]

    filter_group_update = models.FilterGroupUpdate(
        name=name,
        ordered_filter_ids_str=ordered_filter_ids_str,
    )

    try:
        db_filter_group = await crud.filter_group.update(
            db=db, obj_in=filter_group_update, id=filter_group_id
        )
    except crud.RecordNotFoundError:
        alerts.danger.append("FilterGroup not found")
        response = RedirectResponse(url="/filter-groups", status_code=status.HTTP_303_SEE_OTHER)
        response.headers["Method"] = "GET"
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    db_filter_group.filters = filters
    db.commit()

    alerts.success.append("FilterGroup updated")

    response = RedirectResponse(
        f"/filter-group/{db_filter_group.id}", status_code=status.HTTP_303_SEE_OTHER
    )
    response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
    return response


@router.get("/filter-groups/fetch", response_class=HTMLResponse)
async def fetch_all_filter_groups(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Fetch all filter_groups

    Args:
        filter_group_id(str): The filter_group id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Fetches videos and redirects back to /filter_group/filter_group_id.
    """
    alerts = models.Alerts()

    fetch_results = await fetch_all_subscriptions(db=db)

    alerts.success.append(f"Fetched {fetch_results.added_videos} new videos")

    response = RedirectResponse(url="/filter-groups", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="alerts", value=alerts.json(), max_age=5, httponly=True)
    return response


@router.get("/filter-group/{filter_group_id}/fetch", response_class=HTMLResponse)
async def fetch_all_filter_group(
    request: Request,
    filter_group_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Fetch all filter_groups

    Args:
        filter_group_id(str): The filter_group id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Fetches videos and redirects back to /filter_group/filter_group_id.
    """
    alerts = models.Alerts()

    fetch_results = await fetch_filter_group(db=db, filter_group_id=filter_group_id)

    alerts.success.append(f"Fetched {fetch_results.added_videos} new videos")

    response = RedirectResponse(
        url=f"/filter-group/{filter_group_id}", status_code=status.HTTP_303_SEE_OTHER
    )
    response.set_cookie(key="alerts", value=alerts.json(), max_age=5, httponly=True)
    return response


@router.get("/filter-group/{filter_group_id}/{ordered_filter_index}", response_class=HTMLResponse)
@router.get("/filter-group/{filter_group_id}", response_class=HTMLResponse)
async def view_filter_group(
    request: Request,
    filter_group_id: str,
    ordered_filter_index: int = 0,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    View filter_group.

    Args:
        request(Request): The request object
        filter_group_id(str): The filter_group id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: View of the filter_group
    """
    alerts = models.Alerts().from_cookies(request.cookies)
    try:
        db_filter_group = await crud.filter_group.get(db=db, id=filter_group_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("FilterGroup not found")
        response = RedirectResponse("/filter-groups", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    # Get Filter from FilterGroup that will be displayed
    filtered_videos = FilteredVideos()
    filter_group_filtered_videos: list[FilteredVideos] = []
    max_videos = 20
    unread_videos: list[models.Video] = []
    redirect_url = f"/filter-group/{db_filter_group.id}"
    db_filter = None

    ordered_filters = db_filter_group.ordered_filters
    for i, db_filter in enumerate(ordered_filters):
        # Skip to the ordered filter index
        if i < ordered_filter_index:
            continue

        # Get filtered videos
        filtered_videos = await get_filtered_videos(filter_=db_filter, max_videos=20)
        if filtered_videos.videos_not_limited_count == 0:
            continue

        # Remove videos found in previous filters
        for video in filtered_videos.videos.copy():
            if video.id in [video.id for video in unread_videos]:
                filtered_videos.videos.remove(video)
                filtered_videos.videos_limited_count -= 1
                filtered_videos.videos_not_limited_count -= 1

        # Limit the number of videos
        max_videos_from_filtered_videos = max_videos - len(unread_videos)
        if filtered_videos.videos_limited_count > max_videos_from_filtered_videos:
            filtered_videos.videos_limited_count = max_videos_from_filtered_videos
            filtered_videos.videos = filtered_videos.videos[:max_videos_from_filtered_videos]

        # Add unread videos to filter group filtered videos
        unread_videos.extend(filtered_videos.videos)
        filter_group_filtered_videos.append(filtered_videos)

        # if max_video is reached, break
        if len(unread_videos) >= max_videos:
            ordered_filter_index = i
            redirect_url = f"/filter-group/{db_filter_group.id}/{i}"
            break

    # Redirect to /filter_groups if no unread videos in filter_group
    if len(unread_videos) == 0:
        alerts.warning.append(f"No unread videos in '{db_filter_group.name}' filter_group.")
        response = RedirectResponse("/filter-groups", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    # Get total unread videos
    total_unread_videos = str(len(await crud.video.get_unread_videos(db=db)))

    # Get all playlists and tags for Modals
    playlists = await crud.playlist.get_all(db=db)
    playlists.sort(key=lambda x: x.name)

    tags = await crud.tag.get_all(db=db)
    tags.sort(key=lambda x: x.name)

    return templates.TemplateResponse(
        "filter/view.html",
        {
            "request": request,
            "filter_group": db_filter_group,
            "filter_group_filtered_videos": filter_group_filtered_videos,
            "redirect_url": redirect_url,
            "playlists": playlists,
            "tags": tags,
            "total_unread_videos": total_unread_videos,
            "current_user": current_user,
            "alerts": alerts,
        },
    )


@router.get("/filter-group/{filter_group_id}/delete", response_class=HTMLResponse)
async def delete_filter_group(
    filter_group_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Delete FilterGroup view.

    Args:
        filter_group_id(str): The filter_group id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: Form to delete a new filter_group
    """
    alerts = models.Alerts()
    try:
        await crud.filter_group.remove(db=db, id=filter_group_id)
        alerts.success.append("FilterGroup deleted")
    except crud.RecordNotFoundError:
        alerts.danger.append("FilterGroup not found")
    except crud.DeleteError:
        alerts.danger.append("Error deleting filter_group")

    response = RedirectResponse(url="/filter-groups", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="alerts", value=alerts.json(), max_age=5, httponly=True)
    return response
