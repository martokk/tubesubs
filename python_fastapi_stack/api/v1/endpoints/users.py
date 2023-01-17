from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic.networks import EmailStr
from sqlmodel import Session

from python_fastapi_stack import crud, models, settings
from python_fastapi_stack.api import deps
from python_fastapi_stack.core import notify, security

router = APIRouter()

router = APIRouter()
ModelClass = models.User
ModelReadClass = models.UserRead
ModelCreateClass = models.UserCreate
ModelUpdateClass = models.UserUpdate
model_crud = crud.user


@router.get("/", response_model=list[models.UserRead])
async def get_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    _: models.User = Depends(deps.get_current_active_superuser),
) -> list[ModelClass]:
    """
    Retrieve users.

    Args:
        db (Session): database session.
        skip (int): Number of items to skip. Defaults to 0.
        limit (int): Number of items to return. Defaults to 100.
        _ (models.User): Current active user.

    Returns:
        list[ModelClass]: List of objects.
    """
    return await crud.user.get_multi(db=db, skip=skip, limit=limit)


@router.get("/me", response_model=models.UserRead)
async def get_me(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> models.User:
    """
    Get current user.

    Args:
        current_user (models.User): Current active user.

    Returns:
        models.User: Current user.
    """
    return current_user


@router.get("/{id}", response_model=models.UserRead)
async def get_by_id(
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> models.User:
    """
    Get user by id.

    Args:
        id (str): id of the item.
        db (Session): database session.
        current_user (Any): authenticated user.

    Returns:
        ModelClass: Retrieved object.

    Raises:
        HTTPException: if object not found.
    """
    user = await crud.user.get_or_none(db, id=id)
    if user == current_user:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user doesn't have enough privileges",
            )
        return user
    if not crud.user.is_superuser(user_=current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="The user doesn't have enough privileges"
        )
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=models.UserRead)
async def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: models.UserCreateWithPassword,
    _: models.User = Depends(deps.get_current_active_superuser),
) -> models.User:
    """
    Create new user.

    Args:
        db (Session): database session.
        user_in (models.UserCreate): user data.
        _ (models.User): Current active user.

    Returns:
        models.User: Created user.

    Raises:
        HTTPException: if user already exists.
    """
    # Creates user
    try:
        user = await crud.user.create_with_password(db, in_obj=user_in)
    except crud.RecordAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this username/email already exists in the system.",
        ) from e

    # Sends email
    if settings.EMAILS_ENABLED and user_in.email:
        notify.send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return user


@router.post("/open", response_model=models.UserRead)
async def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    username: str = Body(...),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
) -> models.User:
    """
    Create new user without the need to be logged in.

    Args:
        db (Session): database session.
        username (str): username.
        password (str): password.
        email (EmailStr): email.
        full_name (str): full name.

    Returns:
        models.User: Created user.

    Raises:
        HTTPException: if user already exists.
        HTTPException: if open registration is forbidden.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Open user registration is forbidden on this server",
        )
    user = await crud.user.get_or_none(db, username=username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system",
        )
    user_in = models.UserCreateWithPassword(
        username=username, password=password, email=email, full_name=full_name
    )
    user = await crud.user.create_with_password(db, in_obj=user_in)
    return user


@router.patch("/{user_id}", response_model=models.UserRead)
async def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: str,
    user_in: models.UserUpdate,
    _: models.User = Depends(deps.get_current_active_superuser),
) -> models.User:
    """
    Update a user.

    Args:
        db (Session): database session.
        user_id (str): id of the user.
        user_in (models.UserUpdate): user data.
        _ (models.User): Current active user.

    Returns:
        models.UserRead: Updated user.

    Raises:
        HTTPException: if user not found.
    """
    user = await crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist in the system",
        )
    user = await crud.user.update(db, id=user_id, in_obj=user_in)
    return user


@router.put("/me", response_model=models.UserRead)
async def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> models.User:
    """
    Update own user.

    Args:
        db (Session): database session.
        password (str): password.
        full_name (str): full name.
        email (EmailStr): email.
        current_user (models.User): Current active user.

    Returns:
        models.User: Updated user.
    """
    user_in = models.UserUpdate(**current_user.dict())
    if password is not None:
        user_in.hashed_password = security.get_password_hash(password=password)
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = await crud.user.update(db, db_obj=current_user, in_obj=user_in)
    return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    _: models.User = Depends(deps.get_current_active_superuser),
) -> None:
    """
    Delete an item. Only superusers can delete items.

    Args:
        id (str): ID of the item to delete.
        db (Session): database session.
        _ (models.User): Current active superuser.

    Returns:
        None

    Raises:
        HTTPException: if item not found.
    """

    video = await model_crud.get_or_none(id=id, db=db)
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        try:
            return await model_crud.remove(id=id, db=db)
        except crud.RecordNotFoundError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found"
            ) from exc
