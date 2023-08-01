from sqlmodel import Session

from app import models

from .base import BaseCRUD


class PlaylistCRUD(BaseCRUD[models.Playlist, models.PlaylistCreate, models.PlaylistUpdate]):
    ...


playlist = PlaylistCRUD(models.Playlist)
