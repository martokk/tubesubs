from typing import TYPE_CHECKING, Any

import datetime

from pydantic import root_validator
from sqlmodel import Field, Relationship, SQLModel

from app.core.uuid import generate_uuid_random

from .common import TimestampModel

if TYPE_CHECKING:
    from .playlist_item import PlaylistItem  # pragma: no cover


class PlaylistBase(TimestampModel, SQLModel):
    id: str = Field(default=None, primary_key=True, nullable=False)
    name: str | None = Field(default=None)


class Playlist(PlaylistBase, table=True):
    playlist_items: list["PlaylistItem"] = Relationship(
        back_populates="playlist",
        sa_relationship_kwargs={
            "cascade": "all, delete",
        },
    )

    def __repr__(self) -> str:
        return f"Playlist(id={self.id}, name={self.name if self.name else ''}"

    def __hash__(self) -> int:  # pyright: reportIncompatibleVariableOverride=false
        return hash(self.id)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Playlist):
            return self.id == other.id
        return False

    @property
    def feed_url(self) -> str:
        return f"/playlist/{self.id}/feed"


class PlaylistCreate(PlaylistBase):
    @root_validator(pre=True)
    @classmethod
    def set_pre_validation_defaults(cls, values: dict[str, Any]) -> dict[str, Any]:
        playlist_id = generate_uuid_random()
        return {
            **values,
            "id": playlist_id,
            "updated_at": datetime.datetime.now(tz=datetime.timezone.utc),
        }


class PlaylistUpdate(PlaylistBase):
    pass


class PlaylistRead(PlaylistBase):
    pass
