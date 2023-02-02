from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from sqlmodel import Session

from python_fastapi_stack import crud, models
from python_fastapi_stack.views import deps, templates

router = APIRouter()


@router.get("/items", response_class=HTMLResponse)
async def list_items(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Returns HTML response with list of items.

    Args:
        request(Request): The request object
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: HTML page with the items

    """
    # Get alerts dict from cookies
    alerts = models.Alerts().from_cookies(request.cookies)

    items = await crud.item.get_multi(db=db, owner_id=current_user.id)
    return templates.TemplateResponse(
        "item/list.html",
        {"request": request, "items": items, "current_user": current_user, "alerts": alerts},
    )


@router.get("/items/all", response_class=HTMLResponse)
async def list_all_items(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_superuser
    ),
) -> Response:
    """
    Returns HTML response with list of all items from all users.

    Args:
        request(Request): The request object
        db(Session): The database session.
        current_user(User): The authenticated superuser.

    Returns:
        Response: HTML page with the items

    """
    # Get alerts dict from cookies
    alerts = models.Alerts().from_cookies(request.cookies)

    items = await crud.item.get_all(db=db)
    return templates.TemplateResponse(
        "item/list.html",
        {"request": request, "items": items, "current_user": current_user, "alerts": alerts},
    )


@router.get("/item/{item_id}", response_class=HTMLResponse)
async def view_item(
    request: Request,
    item_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    View item.

    Args:
        request(Request): The request object
        item_id(str): The item id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: View of the item
    """
    alerts = models.Alerts()
    try:
        item = await crud.item.get(db=db, id=item_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Item not found")
        response = RedirectResponse("/items", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    return templates.TemplateResponse(
        "item/view.html",
        {"request": request, "item": item, "current_user": current_user, "alerts": alerts},
    )


@router.get("/items/create", response_class=HTMLResponse)
async def create_item(
    request: Request,
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    New Item form.

    Args:
        request(Request): The request object
        current_user(User): The authenticated user.

    Returns:
        Response: Form to create a new item
    """
    alerts = models.Alerts().from_cookies(request.cookies)
    return templates.TemplateResponse(
        "item/create.html",
        {"request": request, "current_user": current_user, "alerts": alerts},
    )


@router.post("/items/create", response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
async def handle_create_item(
    title: str = Form(...),
    description: str = Form(...),
    url: str = Form(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Handles the creation of a new item.

    Args:
        title(str): The title of the item
        description(str): The description of the item
        url(str): The url of the item
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: List of items view
    """
    alerts = models.Alerts()
    item_create = models.ItemCreate(
        title=title, description=description, url=url, owner_id=current_user.id
    )
    try:
        await crud.item.create(db=db, in_obj=item_create)
    except crud.RecordAlreadyExistsError:
        alerts.danger.append("Item already exists")
        response = RedirectResponse("/items/create", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    alerts.success.append("Item successfully created")
    response = RedirectResponse(url="/items", status_code=status.HTTP_303_SEE_OTHER)
    response.headers["Method"] = "GET"
    response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
    return response


@router.get("/item/{item_id}/edit", response_class=HTMLResponse)
async def edit_item(
    request: Request,
    item_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    New Item form.

    Args:
        request(Request): The request object
        item_id(str): The item id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: Form to create a new item
    """
    alerts = models.Alerts().from_cookies(request.cookies)
    try:
        item = await crud.item.get(db=db, id=item_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Item not found")
        response = RedirectResponse("/items", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response
    return templates.TemplateResponse(
        "item/edit.html",
        {"request": request, "item": item, "current_user": current_user, "alerts": alerts},
    )


@router.post("/item/{item_id}/edit", response_class=HTMLResponse)
async def handle_edit_item(
    request: Request,
    item_id: str,
    title: str = Form(...),
    description: str = Form(...),
    url: str = Form(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Handles the creation of a new item.

    Args:
        request(Request): The request object
        item_id(str): The item id
        title(str): The title of the item
        description(str): The description of the item
        url(str): The url of the item
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: View of the newly created item
    """
    alerts = models.Alerts()
    item_update = models.ItemUpdate(title=title, description=description, url=url)

    try:
        new_item = await crud.item.update(db=db, in_obj=item_update, id=item_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Item not found")
        response = RedirectResponse(url="/items", status_code=status.HTTP_303_SEE_OTHER)
        response.headers["Method"] = "GET"
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response
    alerts.success.append("Item updated")
    return templates.TemplateResponse(
        "item/edit.html",
        {"request": request, "item": new_item, "current_user": current_user, "alerts": alerts},
    )


@router.get("/item/{item_id}/delete", response_class=HTMLResponse)
async def delete_item(
    item_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    New Item form.

    Args:
        item_id(str): The item id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: Form to create a new item
    """
    alerts = models.Alerts()
    try:
        await crud.item.remove(db=db, id=item_id)
        alerts.success.append("Item deleted")
    except crud.RecordNotFoundError:
        alerts.danger.append("Item not found")
    except crud.DeleteError:
        alerts.danger.append("Error deleting item")

    response = RedirectResponse(url="/items", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="alerts", value=alerts.json(), max_age=5, httponly=True)
    return response
