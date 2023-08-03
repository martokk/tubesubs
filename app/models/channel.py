from typing import TYPE_CHECKING, Any

import datetime

from pydantic import root_validator
from sqlmodel import Field, Relationship, SQLModel

from app.core.uuid import generate_uuid_from_string
from app.handlers import get_service_handler_from_string
from app.handlers.base import ServiceHandler
from app.models.channel_tag_link import ChannelTagLink

from .common import TimestampModel

if TYPE_CHECKING:
    from .tag import Tag  # pragma: no cover
    from .video import Video  # pragma: no cover


class ChannelBase(TimestampModel, SQLModel):
    id: str = Field(default=None, primary_key=True, nullable=False)
    service_handler: str = Field(default=None, nullable=False)
    remote_channel_id: str = Field(default=None, nullable=False)
    name: str = Field(default=None)
    logo: str | None = Field(default=None)
    is_hidden: bool = Field(default=False)


class Channel(ChannelBase, table=True):
    videos: list["Video"] = Relationship(
        back_populates="channel",
        sa_relationship_kwargs={
            "cascade": "all, delete",
        },
    )

    tags: list["Tag"] = Relationship(
        back_populates="channels",
        link_model=ChannelTagLink,
    )

    def __repr__(self) -> str:
        return f"Channel(id={self.id}, name={self.name if self.name else ''}, remote_channel_id={self.remote_channel_id}, service_handler={self.service_handler})"

    def __hash__(self) -> int:  # pyright: ignore[reportIncompatibleVariableOverride]
        return hash(self.id)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Channel):
            return self.id == other.id
        return False

    @property
    def service_handler_obj(self) -> ServiceHandler:
        return get_service_handler_from_string(handler_string=self.service_handler)

    @property
    def service(self) -> str:
        return self.service_handler_obj.TITLE

    @property
    def url(self) -> str:
        return self.service_handler_obj.get_channel_url(remote_channel_id=self.remote_channel_id)


class ChannelCreate(ChannelBase):
    @root_validator(pre=True)
    @classmethod
    def set_pre_validation_defaults(cls, values: dict[str, Any]) -> dict[str, Any]:
        remote_channel_id = values["remote_channel_id"]
        channel_id = generate_uuid_from_string(string=remote_channel_id)
        return {
            **values,
            "id": channel_id,
            "updated_at": datetime.datetime.now(tz=datetime.timezone.utc),
        }


class ChannelUpdate(ChannelBase):
    pass


class ChannelRead(ChannelBase):
    pass
