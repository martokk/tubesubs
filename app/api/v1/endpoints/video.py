from fastapi import APIRouter, Body, Depends, status
from sqlmodel import Session

from app import crud, models
from app.api import deps
from app.services.videos import mark_videos_as_read

router = APIRouter()
ModelClass = models.PlaylistItem
ModelReadClass = models.PlaylistItemRead
ModelCreateClass = models.PlaylistItemCreate
ModelUpdateClass = models.PlaylistItemUpdate
model_crud = crud.video


@router.post("/mark-videos-read", status_code=status.HTTP_200_OK)
async def handle_mark_videos_read(
    db: Session = Depends(deps.get_db), video_ids: list[str] = Body(..., embed=True)
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

    await mark_videos_as_read(db=db, video_ids=video_ids)
