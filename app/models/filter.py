from typing import TYPE_CHECKING, Any

from enum import Enum

from pydantic import root_validator
from sqlmodel import Field, Relationship, SQLModel

from app.core.uuid import generate_uuid_random
from app.models.filter_filter_group_link import FilterFilterGroupLink
from app.models.subscription_filter_link import SubscriptionFilterLink

from .common import TimestampModel
from .criteria import Criteria

if TYPE_CHECKING:
    from .filter_group import FilterGroup  # pragma: no cover
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
    show_hidden_channels: bool = Field(default=False)


class Filter(FilterBase, table=True):
    criterias: list["Criteria"] = Relationship(
        back_populates="filter", sa_relationship_kwargs={"cascade": "delete"}
    )

    subscriptions: list["Subscription"] = Relationship(
        back_populates="filters",
        link_model=SubscriptionFilterLink,
    )
    filter_groups: list["FilterGroup"] = Relationship(
        back_populates="filters",
        link_model=FilterFilterGroupLink,
    )

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
