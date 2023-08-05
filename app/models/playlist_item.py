from typing import TYPE_CHECKING, Any

import datetime

from pydantic import root_validator
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from app.core.uuid import generate_uuid_random

from .common import TimestampModel

if TYPE_CHECKING:
    from .playlist import Playlist  # pragma: no cover


class PlaylistItemBase(TimestampModel, SQLModel):
    id: str = Field(default=None, primary_key=True, nullable=False)
    title: str | None = Field(default=None)
    url: str | None = Field(default=None)
    thumbnail: str | None = Field(default=None)
    duration: int | None = Field(default=None)
    description: str | None = Field(default=None)
    playlist_id: str = Field(default=None, foreign_key="playlist.id", nullable=False)

    # Define a custom constraint to ensure the uniqueness of url per playlist_id
    __table_args__ = (UniqueConstraint("url", "playlist_id"),)


class PlaylistItem(PlaylistItemBase, table=True):
    playlist: "Playlist" = Relationship()

    def __repr__(self) -> str:
        return f"PlaylistItem(id={self.id}, title={self.title if self.title else ''}"

    def __hash__(self) -> int:  # pyright: ignore[reportIncompatibleVariableOverride]
        return hash(self.id)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, PlaylistItem):
            return self.id == other.id
        return False


class PlaylistItemCreate(PlaylistItemBase):
    @root_validator(pre=True)
    @classmethod
    def set_pre_validation_defaults(cls, values: dict[str, Any]) -> dict[str, Any]:
        playlist_item_id = generate_uuid_random()
        return {
            **values,
            "id": playlist_item_id,
            "updated_at": datetime.datetime.now(tz=datetime.timezone.utc),
        }


class PlaylistItemUpdate(PlaylistItemBase):
    pass


class PlaylistItemRead(PlaylistItemBase):
    pass
