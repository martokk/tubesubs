from typing import TYPE_CHECKING, Any

import datetime

from pydantic import root_validator
from sqlmodel import Field, Relationship, SQLModel

from app.core.uuid import generate_uuid_from_url
from app.handlers import get_service_handler_from_url
from app.models.subscription_video_link import SubscriptionVideoLink

from .common import TimestampModel

if TYPE_CHECKING:
    from .channel import Channel  # pragma: no cover
    from .subscription import Subscription  # pragma: no cover


class VideoBase(TimestampModel, SQLModel):
    id: str = Field(default=None, primary_key=True, nullable=False)
    service_handler: str = Field(
        default=None,
        nullable=False,
    )
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    duration: int | None = Field(default=None)
    thumbnail: str | None = Field(default=None)
    url: str = Field(default=None, nullable=False)
    released_at: datetime.datetime = Field(default=None)
    remote_channel_id: str = Field(
        default=None, foreign_key="channel.remote_channel_id", nullable=False
    )
    remote_channel_name: str = Field(default=None)
    remote_video_id: str | None = Field(default=None)
    is_read: bool = Field(default=False, nullable=False)


class Video(VideoBase, table=True):
    subscriptions: list["Subscription"] = Relationship(
        back_populates="videos",
        link_model=SubscriptionVideoLink,
    )
    channel: "Channel" = Relationship()

    def __repr__(self) -> str:
        return f"Video(id={self.id}, title={self.title[:20] if self.title else ''}, remote_channel_id={self.remote_channel_id}, service_handler={self.service_handler})"

    def __hash__(self) -> int:  # pyright: reportIncompatibleVariableOverride=false
        return hash(self.id)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Video):
            return self.id == other.id
        return False


class VideoCreate(VideoBase):
    @root_validator(pre=True)
    @classmethod
    def set_pre_validation_defaults(cls, values: dict[str, Any]) -> dict[str, Any]:
        service_handler = get_service_handler_from_url(url=values["url"])
        sanitized_url = service_handler.sanitize_video_url(url=values["url"])
        video_id = generate_uuid_from_url(url=sanitized_url)

        return {
            **values,
            "service_handler": service_handler.name,
            "url": sanitized_url,
            "id": video_id,
            "updated_at": datetime.datetime.now(tz=datetime.timezone.utc),
        }


class VideoUpdate(VideoBase):
    pass


class VideoRead(VideoBase):
    pass
