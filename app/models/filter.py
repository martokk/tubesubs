from typing import TYPE_CHECKING, Any

import operator
from enum import Enum

from pydantic import root_validator
from sqlmodel import Field, Relationship, SQLModel

from app.core.uuid import generate_uuid_random
from app.models.subscription_filter_link import SubscriptionFilterLink

from .common import TimestampModel
from .criteria import Criteria, CriteriaField, CriteriaOperator  # pragma: no cover
from .video import Video  # pragma: no cover

if TYPE_CHECKING:
    from .subscription import Subscription  # pragma: no cover


class FilterReadStatus(Enum):
    READ = "read"
    UNREAD = "unread"
    ALL = "all"


class FilterOrderedBy(Enum):
    CREATED_AT = "created_at"


class FilterBase(TimestampModel, SQLModel):
    id: str = Field(default=None, primary_key=True, index=True)
    name: str = Field(default=None)
    ordered_by: str = Field(default=FilterOrderedBy.CREATED_AT.value)
    reverse_order: bool = Field(default=False)
    read_status: str = Field(
        default=FilterReadStatus.ALL.value,
    )


class Filter(FilterBase, table=True):
    criterias: list["Criteria"] = Relationship(
        back_populates="filter", sa_relationship_kwargs={"cascade": "delete"}
    )

    subscriptions: list["Subscription"] = Relationship(
        back_populates="filters",
        link_model=SubscriptionFilterLink,
    )

    def get_videos(self, max_videos: int) -> list[Video]:
        def sort_order_by(
            videos: list[Video],
            order_by: str = FilterOrderedBy.CREATED_AT.value,
            reverse: bool = False,
        ) -> list[Video]:
            return sorted(videos, key=lambda video: getattr(video, order_by), reverse=reverse)

        # Get videos
        videos = self._get_videos_from_subscriptions()

        # Filter
        if self.read_status == FilterReadStatus.READ.value:
            videos = [video for video in videos if video.is_read is True]
        if self.read_status == FilterReadStatus.UNREAD.value:
            videos = [video for video in videos if video.is_read is False]

        # Order By sort
        videos = sort_order_by(
            videos=videos, order_by=FilterOrderedBy.CREATED_AT.value, reverse=self.reverse_order
        )

        # Limit Videos
        videos = videos[:max_videos]

        return videos

    def _get_videos_from_subscriptions(self) -> list[Video]:
        videos = []
        for subscription in self.subscriptions:
            videos.extend(subscription.videos)
        return videos

    @property
    def subscriptions_as_strings(self) -> list[str]:
        subscriptions = [subscription.subscription_handler for subscription in self.subscriptions]
        return subscriptions

    @property
    def feed_url(self) -> str:
        return f"/filter/{self.id}/feed"


class FilterCreate(FilterBase, TimestampModel):
    @root_validator(pre=True)
    @classmethod
    def set_pre_validation_defaults(cls, values: dict[str, Any]) -> dict[str, Any]:
        filter_id = generate_uuid_random()
        return {
            **values,
            "id": filter_id,
        }


class FilterUpdate(FilterBase):
    pass


class FilterRead(FilterBase):
    criterias: list["Criteria"] = Relationship()
