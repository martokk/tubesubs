from collections.abc import Generator

from fastapi import Cookie, Depends, HTTPException, status
from sqlmodel import Session

from python_fastapi_stack import crud, models, settings
from python_fastapi_stack.core import security
from python_fastapi_stack.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    A generator function that creates a new database session.

    Yields:
        Session: A new database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_access_token_from_cookie(access_token: str | None = Cookie(None)) -> str | None:
    """
    Gets the access token from the cookie.

    Args:
        access_token (str | None): The access token.

    Returns:
        str | None: The access token.
    """
    if access_token and "Bearer" in access_token:
        return access_token.split("Bearer ")[1]
    return None


async def get_current_user(
    access_token: str | None = Depends(get_access_token_from_cookie), db: Session = Depends(get_db)
) -> models.User | None:
    """
    Gets the current user. If the access token is
    invalid or not found in cookie, returns None.

    Args:
        access_token (str | None): The access token.
        db (Session): The database session.

    Returns:
        models.User | None: The current user.
    """
    if not access_token:
        return None
    try:
        user_id = security.decode_token(token=access_token, key=settings.JWT_ACCESS_SECRET_KEY)
    except HTTPException:
        return None
    return await crud.user.get(db=db, id=user_id)


async def get_current_user_or_raise(
    current_user: models.User | None = Depends(get_current_user),
) -> models.User | None:
    """
    Gets the current user or raises 401

    """
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return current_user


async def get_current_active_user(
    current_user: models.User = Depends(get_current_user_or_raise),
) -> models.User:
    """
    Gets the current active user.

    Args:
        current_user (models.User): The current user.

    Returns:
        models.User: The current active user.

    Raises:
        HTTPException: If the user is inactive.
    """
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user_or_raise),
) -> models.User:
    """
    Gets the current active superuser.

    Args:
        current_user (models.User): The current user.

    Returns:
        models.User: The current active superuser.

    Raises:
        HTTPException: If the user is not a superuser.
    """
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    if not crud.user.is_superuser(user_=current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="The user doesn't have enough privileges"
        )
    return current_user
