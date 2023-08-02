from fastapi import APIRouter, BackgroundTasks, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from sqlmodel import Session

from app import crud, models
from app.handlers import get_registered_subscription_handlers, get_subscription_handler_from_string
from app.services.fetch import fetch_subscription
from app.views import deps, templates

router = APIRouter()


@router.get("/subscriptions", response_class=HTMLResponse)
async def list_subscriptions(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Returns HTML response with list of subscriptions.

    Args:
        request(Request): The request object
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: HTML page with the subscriptions

    """
    # Get alerts dict from cookies
    alerts = models.Alerts().from_cookies(request.cookies)

    subscriptions = await crud.subscription.get_all(db=db)
    return templates.TemplateResponse(
        "subscription/list.html",
        {
            "request": request,
            "subscriptions": subscriptions,
            "current_user": current_user,
            "alerts": alerts,
        },
    )


@router.get("/subscriptions/all", response_class=HTMLResponse)
async def list_all_subscriptions(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_superuser
    ),
) -> Response:
    """
    Returns HTML response with list of all subscriptions from all users.

    Args:
        request(Request): The request object
        db(Session): The database session.
        current_user(User): The authenticated superuser.

    Returns:
        Response: HTML page with the subscriptions

    """
    # Get alerts dict from cookies
    alerts = models.Alerts().from_cookies(request.cookies)

    subscriptions = await crud.subscription.get_all(db=db)
    return templates.TemplateResponse(
        "subscription/list.html",
        {
            "request": request,
            "subscriptions": subscriptions,
            "current_user": current_user,
            "alerts": alerts,
        },
    )


@router.get("/subscription/create", response_class=HTMLResponse)
async def create_subscription(
    request: Request,
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    New Subscription form.

    Args:
        request(Request): The request object
        current_user(User): The authenticated user.

    Returns:
        Response: Form to create a new subscription
    """
    alerts = models.Alerts().from_cookies(request.cookies)
    subscription_handlers = get_registered_subscription_handlers()

    return templates.TemplateResponse(
        "subscription/create.html",
        {
            "request": request,
            "current_user": current_user,
            "alerts": alerts,
            "subscription_handlers": subscription_handlers,
        },
    )


@router.post(
    "/subscription/create", response_class=HTMLResponse, status_code=status.HTTP_201_CREATED
)
async def handle_create_subscription(
    subscription_handler: str = Form(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Handles the creation of a new subscription.

    Args:
        service_handler(str): The service_handler of the subscription
        subscription_handler(str): The subscription_handler of the subscription
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: List of subscriptions view
    """
    alerts = models.Alerts()

    handler = get_subscription_handler_from_string(handler_string=subscription_handler)

    try:
        subscription_create = models.SubscriptionCreate(
            service_handler=handler.SERVICE,
            subscription_handler=subscription_handler,
            created_by=current_user.id,
        )
    except ValueError as e:
        alerts.danger.append(e.args[0][0].exc.args[0])
        response = RedirectResponse("/subscription/create", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    try:
        await crud.subscription.create(db=db, obj_in=subscription_create)
    except crud.RecordAlreadyExistsError:
        alerts.danger.append("Subscription already exists")
        response = RedirectResponse("/subscription/create", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    alerts.success.append("Subscription successfully created")
    response = RedirectResponse(url="/subscriptions", status_code=status.HTTP_303_SEE_OTHER)
    response.headers["Method"] = "GET"
    response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
    return response


@router.get("/subscription/{subscription_id}", response_class=HTMLResponse)
async def view_subscription(
    request: Request,
    subscription_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    View subscription.

    Args:
        request(Request): The request object
        subscription_id(str): The subscription id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: View of the subscription
    """
    alerts = models.Alerts()
    try:
        subscription = await crud.subscription.get(db=db, id=subscription_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Subscription not found")
        response = RedirectResponse("/subscriptions", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    return templates.TemplateResponse(
        "subscription/view.html",
        {
            "request": request,
            "subscription": subscription,
            "current_user": current_user,
            "alerts": alerts,
        },
    )


@router.get("/subscription/{subscription_id}/edit", response_class=HTMLResponse)
async def edit_subscription(
    request: Request,
    subscription_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Edit subscription form.

    Args:
        request(Request): The request object
        subscription_id(str): The subscription id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: Form to edit a subscription
    """
    alerts = models.Alerts().from_cookies(request.cookies)
    try:
        subscription = await crud.subscription.get(db=db, id=subscription_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Subscription not found")
        response = RedirectResponse("/subscriptions", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response
    return templates.TemplateResponse(
        "subscription/edit.html",
        {
            "request": request,
            "subscription": subscription,
            "current_user": current_user,
            "alerts": alerts,
        },
    )


@router.post("/subscription/{subscription_id}/edit", response_class=HTMLResponse)
async def handle_edit_subscription(
    request: Request,
    subscription_id: str,
    service_handler: str = Form(...),
    subscription_handler: str = Form(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Handles the edit of a subscription.

    Args:
        request(Request): The request object
        subscription_id(str): The subscription id
        service_handler(str): The service_handler of the subscription
        subscription_handler(str): The subscription_handler of the subscription
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: View of the edited subscription
    """
    alerts = models.Alerts()
    subscription_update = models.SubscriptionUpdate(
        service_handler=service_handler, subscription_handler=subscription_handler
    )

    try:
        new_subscription = await crud.subscription.update(
            db=db, obj_in=subscription_update, id=subscription_id
        )
    except crud.RecordNotFoundError:
        alerts.danger.append("Subscription not found")
        response = RedirectResponse(url="/subscriptions", status_code=status.HTTP_303_SEE_OTHER)
        response.headers["Method"] = "GET"
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response
    alerts.success.append("Subscription updated")
    return templates.TemplateResponse(
        "subscription/edit.html",
        {
            "request": request,
            "subscription": new_subscription,
            "current_user": current_user,
            "alerts": alerts,
        },
    )


@router.get("/subscription/{subscription_id}/delete", response_class=HTMLResponse)
async def delete_subscription(
    subscription_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Delete Subscription view.

    Args:
        subscription_id(str): The subscription id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: Form to delete a new subscription
    """
    alerts = models.Alerts()
    try:
        await crud.subscription.remove(db=db, id=subscription_id)
        alerts.success.append("Subscription deleted")
    except crud.RecordNotFoundError:
        alerts.danger.append("Subscription not found")
    except crud.DeleteError:
        alerts.danger.append("Error deleting subscription")

    response = RedirectResponse(url="/subscriptions", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="alerts", value=alerts.json(), max_age=5, httponly=True)
    return response


@router.get("/subscription/{subscription_id}/fetch", response_class=HTMLResponse)
async def fetch_subscription_page(
    background_tasks: BackgroundTasks,
    subscription_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Fetch Subscription Videos

    Args:
        subscription_id(str): The subscription id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Fetches videos and redirects back to /subscriptions.
    """
    alerts = models.Alerts()
    try:
        subscription = await crud.subscription.get(db=db, id=subscription_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Subscription not found")
        response = RedirectResponse("/subscriptions", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    background_tasks.add_task(
        fetch_subscription,
        id=subscription.id,
        db=db,
    )
    alerts.success.append(f"Subscription '{subscription.title}' was fetched.")

    response = RedirectResponse(
        url=f"/subscription/{subscription.id}", status_code=status.HTTP_303_SEE_OTHER
    )
    response.set_cookie(key="alerts", value=alerts.json(), max_age=5, httponly=True)
    return response
