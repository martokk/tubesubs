from fastapi import APIRouter, BackgroundTasks, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from sqlmodel import Session

from app import crud, models
from app.handlers import get_registered_subscription_handlers
from app.services.fetch import fetch_all_subscriptions, fetch_filter
from app.services.filter_videos import get_filtered_videos
from app.services.videos import mark_videos_as_read
from app.views import deps, templates

# from app.services.fetch import fetch_filter

router = APIRouter()


@router.get("/filters", response_class=HTMLResponse)
async def list_filters(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Returns HTML response with list of filters.

    Args:
        request(Request): The request object
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: HTML page with the filters

    """
    # Get alerts dict from cookies
    alerts = models.Alerts().from_cookies(request.cookies)

    # Get all filters
    filters = await crud.filter.get_all(db=db)
    filters.sort(key=lambda x: x.name)

    # Get unread count for each filter
    filters_unread_count = {}
    for filter_ in filters:
        filtered_videos = await get_filtered_videos(filter_=filter_)
        filters_unread_count[filter_.id] = filtered_videos.videos_not_limited_count

    # Seperate read filters
    read_filters = []
    for filter_ in filters.copy():
        filter_unread_count = int(filters_unread_count[filter_.id])
        if filter_unread_count == 0:
            read_filters.append(filter_)
            filters.remove(filter_)

    # Separate pinned filters
    pinned_filter_names = ["All Unread", "Missing Tags"]
    pinned_filters = []
    for filter_ in filters:
        if filter_.name in pinned_filter_names:
            pinned_filters.append(filter_)
            filters.remove(filter_)

    return templates.TemplateResponse(
        "filter/list.html",
        {
            "request": request,
            "read_filters": read_filters,
            "pinned_filters": pinned_filters,
            "filters": filters,
            "filters_unread_count": filters_unread_count,
            "current_user": current_user,
            "alerts": alerts,
        },
    )


@router.get("/filters/all", response_class=HTMLResponse)
async def list_all_filters(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Returns HTML response with list of all filters from all users.

    Args:
        request(Request): The request object
        db(Session): The database session.
        current_user(User): The authenticated superuser.

    Returns:
        Response: HTML page with the filters

    """
    # Get alerts dict from cookies
    alerts = models.Alerts().from_cookies(request.cookies)

    filters = await crud.filter.get_all(db=db)
    return templates.TemplateResponse(
        "filter/list.html",
        {
            "request": request,
            "filters": filters,
            "current_user": current_user,
            "alerts": alerts,
        },
    )


@router.get("/filter/create", response_class=HTMLResponse)
async def create_filter(
    request: Request,
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    New Filter form.

    Args:
        request(Request): The request object
        current_user(User): The authenticated user.

    Returns:
        Response: Form to create a new filter
    """
    alerts = models.Alerts().from_cookies(request.cookies)
    options_subscription_handlers = get_registered_subscription_handlers()
    options_ordered_by = [option.value for option in models.FilterOrderedBy]
    options_read_status = [option.value for option in models.FilterReadStatus]

    return templates.TemplateResponse(
        "filter/create.html",
        {
            "request": request,
            "current_user": current_user,
            "alerts": alerts,
            "options_subscription_handlers": options_subscription_handlers,
            "options_ordered_by": options_ordered_by,
            "options_read_status": options_read_status,
        },
    )


@router.post("/filter/create", response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
async def handle_create_filter(
    name: str = Form(...),
    subscription_handlers: list[str] = Form(...),
    read_status: str = Form(...),
    ordered_by: str = Form(...),
    reverse_order: bool = Form(False),
    show_hidden_channels: bool = Form(False),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Handles the creation of a new filter.

    Args:
        name(str): Name of the Filter
        subscription_handlers(list[str]): The subscription_handlers of the filter
        read_status(str): read_status of the Filter
        ordered_by(str): ordered_by of the Filter
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: List of filters view
    """
    alerts = models.Alerts()

    # Create Filter and Save in Database
    try:
        filter_create = models.FilterCreate(
            name=name,
            ordered_by=ordered_by,
            read_status=read_status,
            reverse_order=reverse_order,
            show_hidden_channels=show_hidden_channels,
        )
    except ValueError as e:
        alerts.danger.append(e.args[0][0].exc.args[0])
        response = RedirectResponse("/filter/create", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    try:
        db_filter = await crud.filter.create(db=db, obj_in=filter_create)
    except crud.RecordAlreadyExistsError:
        alerts.danger.append("Filter already exists")
        response = RedirectResponse("/filter/create", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    # Add Subscriptions to filter
    subscriptions = [
        await crud.subscription.get(db=db, subscription_handler=subscription_handler)
        for subscription_handler in subscription_handlers
    ]

    db_filter = await crud.filter.add_subscriptions(
        db=db, filter_id=db_filter.id, subscriptions=subscriptions
    )

    # Redirect on Success
    alerts.success.append("Filter successfully created")
    response = RedirectResponse(
        url=f"/filter/{db_filter.id}/edit", status_code=status.HTTP_303_SEE_OTHER
    )
    response.headers["Method"] = "GET"
    response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
    return response


@router.get("/filter/{filter_id}", response_class=HTMLResponse)
async def view_filter(
    request: Request,
    filter_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    View filter.

    Args:
        request(Request): The request object
        filter_id(str): The filter id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: View of the filter
    """
    alerts = models.Alerts().from_cookies(request.cookies)
    try:
        db_filter = await crud.filter.get(db=db, id=filter_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Filter not found")
        response = RedirectResponse("/filters", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    filtered_videos = await get_filtered_videos(filter_=db_filter, max_videos=20)

    # Redirect to /filters if no unread videos in filter
    if filtered_videos.videos_not_limited_count == 0:
        alerts.warning.append(f"No unread videos in '{db_filter.name}' filter.")
        response = RedirectResponse("/filters", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    playlists = await crud.playlist.get_all(db=db)
    playlists.sort(key=lambda x: x.name)

    tags = await crud.tag.get_all(db=db)
    tags.sort(key=lambda x: x.name)

    redirect_url = f"/filter/{filter_id}"

    return templates.TemplateResponse(
        "filter/view.html",
        {
            "request": request,
            "filter": db_filter,
            "filtered_videos": filtered_videos,
            "redirect_url": redirect_url,
            "playlists": playlists,
            "tags": tags,
            "current_user": current_user,
            "alerts": alerts,
        },
    )


@router.get("/filter/{filter_id}/edit", response_class=HTMLResponse)
async def edit_filter(
    request: Request,
    filter_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Edit filter form.

    Args:
        request(Request): The request object
        filter_id(str): The filter id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: Form to edit a filter
    """
    alerts = models.Alerts().from_cookies(request.cookies)
    try:
        db_filter = await crud.filter.get(db=db, id=filter_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Filter not found")
        response = RedirectResponse("/filters", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    # Build Filter Options
    options_subscription_handlers = get_registered_subscription_handlers()
    options_ordered_by = [option.value for option in models.FilterOrderedBy]
    options_read_status = [option.value for option in models.FilterReadStatus]

    # Build Criterias Options
    options_criteria_fields = list(attr.value for attr in models.CriteriaField)
    options_created_at_operators = [
        models.CriteriaOperator.WITHIN.value,
        models.CriteriaOperator.AFTER.value,
    ]
    options_duration_operators = [
        models.CriteriaOperator.SHORTER_THAN.value,
        models.CriteriaOperator.LONGER_THAN.value,
    ]
    options_keyword_operators = [
        models.CriteriaOperator.MUST_CONTAIN.value,
        models.CriteriaOperator.MUST_NOT_CONTAIN.value,
    ]
    options_read_status_operators = [
        models.CriteriaOperator.IS.value,
    ]
    options_channel_id_operators = [
        models.CriteriaOperator.IS.value,
        models.CriteriaOperator.IS_NOT.value,
    ]
    options_channel_operators = [
        models.CriteriaOperator.MUST_CONTAIN.value,
        models.CriteriaOperator.MUST_NOT_CONTAIN.value,
    ]
    options_priority_operators = [
        models.CriteriaOperator.LESS_THAN.value,
        models.CriteriaOperator.EQUAL_TO.value,
        models.CriteriaOperator.GREATER_THAN.value,
    ]

    options_read_status_values = [
        models.CriteriaValue.UNREAD.value,
        models.CriteriaValue.READ.value,
    ]

    all_tags = await crud.tag.get_all(db=db)
    all_tags.sort(key=lambda x: x.name)
    options_tag_values = [tag.name for tag in all_tags]
    options_tag_values.append("ANY")

    return templates.TemplateResponse(
        "filter/edit.html",
        {
            "request": request,
            "filter": db_filter,
            "current_user": current_user,
            "alerts": alerts,
            "options_subscription_handlers": options_subscription_handlers,
            "options_ordered_by": options_ordered_by,
            "options_read_status": options_read_status,
            "options_criteria_fields": options_criteria_fields,
            "options_created_at_operators": options_created_at_operators,
            "options_duration_operators": options_duration_operators,
            "options_keyword_operators": options_keyword_operators,
            "options_read_status_operators": options_read_status_operators,
            "options_channel_id_operators": options_channel_id_operators,
            "options_channel_operators": options_channel_operators,
            "options_priority_operators": options_priority_operators,
            "options_read_status_values": options_read_status_values,
            "options_tag_values": options_tag_values,
        },
    )


@router.post("/filter/{filter_id}/edit", response_class=HTMLResponse)
async def handle_edit_filter(
    request: Request,
    filter_id: str,
    name: str = Form(...),
    subscription_handlers: list[str] = Form(...),
    read_status: str = Form(...),
    ordered_by: str = Form(...),
    reverse_order: bool = Form(False),
    show_hidden_channels: bool = Form(False),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Handles the edit of a filter.

    Args:
        request(Request): The request object
        filter_id(str): The filter id
        service_handler(str): The service_handler of the filter
        filter_handler(str): The filter_handler of the filter
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: View of the edited filter
    """
    alerts = models.Alerts()
    filter_update = models.FilterUpdate(
        name=name,
        ordered_by=ordered_by,
        read_status=read_status,
        reverse_order=reverse_order,
        show_hidden_channels=show_hidden_channels,
    )

    try:
        db_filter = await crud.filter.update(db=db, obj_in=filter_update, id=filter_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Filter not found")
        response = RedirectResponse(url="/filters", status_code=status.HTTP_303_SEE_OTHER)
        response.headers["Method"] = "GET"
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    # Update Subscriptions
    subscriptions = [
        await crud.subscription.get(db=db, subscription_handler=subscription_handler)
        for subscription_handler in subscription_handlers
    ]

    db_filter = await crud.filter.update_subscriptions(
        db=db, filter_id=db_filter.id, subscriptions=subscriptions
    )

    alerts.success.append("Filter updated")

    response = RedirectResponse(f"/filter/{filter_id}/edit", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
    return response


@router.get("/filter/{filter_id}/delete", response_class=HTMLResponse)
async def delete_filter(
    filter_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Delete Filter view.

    Args:
        filter_id(str): The filter id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: Form to delete a new filter
    """
    alerts = models.Alerts()
    try:
        await crud.filter.remove(db=db, id=filter_id)
        alerts.success.append("Filter deleted")
    except crud.RecordNotFoundError:
        alerts.danger.append("Filter not found")
    except crud.DeleteError:
        alerts.danger.append("Error deleting filter")

    response = RedirectResponse(url="/filters", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="alerts", value=alerts.json(), max_age=5, httponly=True)
    return response


# @router.get("/filter/{filter_id}/fetch", response_class=HTMLResponse)
# async def fetch_filter_page(
#     background_tasks: BackgroundTasks,
#     filter_id: str,
#     db: Session = Depends(deps.get_db),
#     current_user: models.User = Depends(  # pylint: disable=unused-argument
#         deps.get_current_active_user
#     ),
# ) -> Response:


@router.get("/filters/fetch", response_class=HTMLResponse)
async def fetch_all_filters(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Fetch all filters

    Args:
        filter_id(str): The filter id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Fetches videos and redirects back to /filter/filter_id.
    """
    alerts = models.Alerts()

    fetch_results = await fetch_all_subscriptions(db=db)

    alerts.success.append(f"Fetched {fetch_results.added_videos} new videos")

    response = RedirectResponse(url="/filters", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="alerts", value=alerts.json(), max_age=5, httponly=True)
    return response


@router.get("/filter/{filter_id}/fetch", response_class=HTMLResponse)
async def fetch_filter_page(
    background_tasks: BackgroundTasks,
    filter_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Fetch filter Videos

    Args:
        filter_id(str): The filter id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Fetches videos and redirects back to /filter/filter_id.
    """
    alerts = models.Alerts()
    try:
        db_filter = await crud.filter.get(db=db, id=filter_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Filter not found")
        response = RedirectResponse("/filters", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    fetch_results = await fetch_filter(db=db, filter_id=filter_id)

    alerts.success.append(f"Fetched {fetch_results.added_videos} new videos")

    response = RedirectResponse(
        url=f"/filter/{db_filter.id}", status_code=status.HTTP_303_SEE_OTHER
    )
    response.set_cookie(key="alerts", value=alerts.json(), max_age=5, httponly=True)
    return response
