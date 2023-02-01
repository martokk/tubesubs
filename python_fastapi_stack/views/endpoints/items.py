from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from python_fastapi_stack import crud, models
from python_fastapi_stack.paths import TEMPLATES_PATH
from python_fastapi_stack.views import deps

router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_PATH)


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

    items = await crud.item.get_multi(db=db, owner_id=current_user.id)
    return templates.TemplateResponse(
        "item/list.html", {"request": request, "items": items, "current_user": current_user}
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

    Raises:
        HTTPException: If the item is not found.
    """
    try:
        item = await crud.item.get(db=db, id=item_id)
    except crud.RecordNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return templates.TemplateResponse(
        "item/view.html", {"request": request, "item": item, "current_user": current_user}
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
    return templates.TemplateResponse(
        "item/create.html", {"request": request, "current_user": current_user}
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
        Response: View of the newly created item

    Raises:
        HTTPException: If the item already exists
    """
    item_create = models.ItemCreate(
        title=title, description=description, url=url, owner_id=current_user.id
    )
    try:
        new_item = await crud.item.create(db=db, in_obj=item_create)
    except crud.RecordAlreadyExistsError as exc:
        raise HTTPException(
            detail="Item already exists", status_code=status.HTTP_400_BAD_REQUEST
        ) from exc

    r = RedirectResponse(url=f"/item/{new_item.id}/edit", status_code=status.HTTP_303_SEE_OTHER)
    r.headers["Method"] = "GET"
    return r


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
    item = await crud.item.get(db=db, id=item_id)
    return templates.TemplateResponse(
        "item/edit.html", {"request": request, "item": item, "current_user": current_user}
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
    item_update = models.ItemUpdate(title=title, description=description, url=url)
    new_item = await crud.item.update(db=db, in_obj=item_update, id=item_id)
    return templates.TemplateResponse(
        "item/edit.html", {"request": request, "item": new_item, "current_user": current_user}
    )


@router.post("/item/{item_id}/delete", response_class=HTMLResponse)
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
    await crud.item.remove(db=db, id=item_id)
    return RedirectResponse(url="/items", status_code=status.HTTP_204_NO_CONTENT)
