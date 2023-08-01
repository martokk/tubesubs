from sqlmodel import Session

from app import models

from .base import BaseCRUD


class PlaylistItemCRUD(
    BaseCRUD[models.PlaylistItem, models.PlaylistItemCreate, models.PlaylistItemUpdate]
):
    ...


playlist_item = PlaylistItemCRUD(models.PlaylistItem)
