from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlmodel import Session

from app import crud, models
from app.api import deps

router = APIRouter()
ModelClass = models.PlaylistItem
ModelReadClass = models.PlaylistItemRead
ModelCreateClass = models.PlaylistItemCreate
ModelUpdateClass = models.PlaylistItemUpdate
model_crud = crud.video


@router.post("/hide", status_code=status.HTTP_201_CREATED)
async def handle_hide_channel(
    db: Session = Depends(deps.get_db),
    channel_id: str = Body(..., embed=True),
) -> None:
    """
    Handles 'hide channel' call

    Args:
        channel_id (str): channel_id of the channel to hide.
        db (Session): Database session.

    Returns:
        HTTP 201 Created

    Raises:
        HTTPException: if object already exists.
    """

    try:
        channel = await crud.channel.get(db=db, id=channel_id)
    except crud.RecordNotFoundError:
        raise HTTPException(detail="Channel does not exist", status_code=status.HTTP_404_NOT_FOUND)

    channel_update = models.ChannelUpdate(is_hidden=True)
    await crud.channel.update(db=db, id=channel.id, obj_in=channel_update)


@router.post("/add_tag", status_code=status.HTTP_201_CREATED)
async def handle_add_tag(
    db: Session = Depends(deps.get_db),
    channel_id: str = Body(..., embed=True),
    tag_id: str = Body(..., embed=True),
) -> None:
    """
    Handles 'add tag' call

    Args:
        channel_id (str): channel_id of the channel to hide.
        db (Session): Database session.

    Returns:
        HTTP 201 Created

    Raises:
        HTTPException: if object already exists.
    """

    # Check if tag already exists for channel
    try:
        db_channel = await crud.channel.get(db=db, id=channel_id)
    except crud.RecordNotFoundError:
        raise HTTPException(detail="Channel does not exist", status_code=status.HTTP_404_NOT_FOUND)

    try:
        db_tag = await crud.tag.get(db=db, id=tag_id)
    except crud.RecordNotFoundError:
        raise HTTPException(detail="Tag does not exist", status_code=status.HTTP_404_NOT_FOUND)

    if db_tag in db_channel.tags:
        raise HTTPException(
            detail="Tag already exists for channel", status_code=status.HTTP_409_CONFLICT
        )

    try:
        await crud.channel.add_tag(db=db, channel_id=channel_id, tag_id=tag_id)
    except crud.RecordNotFoundError:
        raise HTTPException(detail="Channel does not exist", status_code=status.HTTP_404_NOT_FOUND)


@router.post("/remove_tag", status_code=status.HTTP_201_CREATED)
async def handle_remove_tag(
    db: Session = Depends(deps.get_db),
    channel_id: str = Body(..., embed=True),
    tag_id: str = Body(..., embed=True),
) -> None:
    """
    Handles 'remove tag' call

    Args:
        channel_id (str): channel_id of the channel to hide.
        db (Session): Database session.

    Returns:
        HTTP 201 Created

    Raises:
        HTTPException: if object already exists.
    """

    # Check if tag already exists for channel
    try:
        db_channel = await crud.channel.get(db=db, id=channel_id)
    except crud.RecordNotFoundError:
        raise HTTPException(detail="Channel does not exist", status_code=status.HTTP_404_NOT_FOUND)

    try:
        db_tag = await crud.tag.get(db=db, id=tag_id)
    except crud.RecordNotFoundError:
        raise HTTPException(detail="Tag does not exist", status_code=status.HTTP_404_NOT_FOUND)

    if db_tag not in db_channel.tags:
        raise HTTPException(
            detail="Tag does not exist for channel", status_code=status.HTTP_409_CONFLICT
        )

    try:
        await crud.channel.delete_tag(db=db, channel_id=channel_id, tag_id=tag_id)
    except crud.RecordNotFoundError:
        raise HTTPException(detail="Channel does not exist", status_code=status.HTTP_404_NOT_FOUND)


# @router.get("/{id}", response_model=ModelReadClass)
# async def get(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: str,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> ModelClass:
#     """
#     Retrieve a video by id.

#     Args:
#         id (str): id of the video.
#         db (Session): database session.
#         current_user (Any): authenticated user.

#     Returns:
#         ModelClass: Retrieved object.

#     Raises:
#         HTTPException: if object does not exist.
#         HTTPException: if user is not superuser and object does not belong to user.
#     """
#     video = await model_crud.get_or_none(id=id, db=db)
#     if video:
#         if crud.user.is_superuser(user_=current_user) or video.owner_id == current_user.id:
#             return video

#     elif crud.user.is_superuser(user_=current_user):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
#     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")


# @router.get("/", response_model=list[ModelReadClass])
# async def get_multi(
#     *,
#     db: Session = Depends(deps.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> list[ModelClass]:
#     """
#     Retrieve videos.

#     Args:
#         db (Session): database session.
#         skip (int): Number of videos to skip. Defaults to 0.
#         limit (int): Number of videos to return. Defaults to 100.
#         current_user (models.User): Current active user.

#     Returns:
#         list[ModelClass]: List of objects.
#     """
#     return (
#         await model_crud.get_multi(db=db, skip=skip, limit=limit)
#         if crud.user.is_superuser(user_=current_user)
#         else await model_crud.get_multi_by_owner_id(
#             db=db, owner_id=current_user.id, skip=skip, limit=limit
#         )
#     )


# @router.patch("/{id}", response_model=ModelReadClass)
# async def update(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: str,
#     obj_in: ModelUpdateClass,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> ModelClass:
#     """
#     Update an video.

#     Args:
#         id (str): ID of the video to update.
#         obj_in (ModelUpdateClass): object to update.
#         db (Session): database session.
#         current_user (Any): authenticated user.

#     Returns:
#         ModelClass: Updated object.

#     Raises:
#         HTTPException: if object not found.
#     """
#     video = await model_crud.get_or_none(id=id, db=db)
#     if video:
#         if crud.user.is_superuser(user_=current_user) or video.owner_id == current_user.id:
#             return await model_crud.update(db=db, obj_in=obj_in, id=id)

#     elif crud.user.is_superuser(user_=current_user):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
#     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")


# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: str,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> None:
#     """
#     Delete an video.

#     Args:
#         id (str): ID of the video to delete.
#         db (Session): database session.
#         current_user (models.User): authenticated user.

#     Returns:
#         None

#     Raises:
#         HTTPException: if video not found.
#     """

#     video = await model_crud.get_or_none(id=id, db=db)
#     if video:
#         if crud.user.is_superuser(user_=current_user) or video.owner_id == current_user.id:
#             return await model_crud.remove(id=id, db=db)

#     elif crud.user.is_superuser(user_=current_user):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
#     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
