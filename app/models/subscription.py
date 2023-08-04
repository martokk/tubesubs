from typing import TYPE_CHECKING, Any

import datetime

from pydantic import root_validator
from sqlmodel import Field, Relationship, SQLModel, desc

from app.core.uuid import generate_uuid_from_string
from app.handlers import (
    get_registered_service_handlers,
    get_registered_subscription_handlers,
    get_service_handler_from_string,
    get_subscription_handler_from_string,
)
from app.handlers.base import ServiceHandler, SubscriptionHandler
from app.models.subscription_filter_link import SubscriptionFilterLink
from app.models.subscription_video_link import SubscriptionVideoLink

from .common import TimestampModel
from .video import Video  # pragma: no cover

if TYPE_CHECKING:
    from .filter import Filter  # pragma: no cover
    from .user import User  # pragma: no cover


class SubscriptionBase(TimestampModel, SQLModel):
    id: str = Field(default=None, primary_key=True, nullable=False)
    created_by: str = Field(default=None, foreign_key="user.id", nullable=False)
    service_handler: str = Field(default=None)
    subscription_handler: str = Field(default=None)


class Subscription(SubscriptionBase, table=True):
    videos: list["Video"] = Relationship(
        back_populates="subscriptions",
        link_model=SubscriptionVideoLink,
        sa_relationship_kwargs={"order_by": desc("created_at"), "cascade": "delete"},
    )
    created_user: "User" = Relationship()

    filters: list["Filter"] = Relationship(
        back_populates="subscriptions",
        link_model=SubscriptionFilterLink,
        sa_relationship_kwargs={"order_by": desc("created_at"), "cascade": "delete"},
    )

    def __repr__(self) -> str:
        return f"Subscription(id={self.id}, service_handler={self.service_handler}, subscription_handler={self.subscription_handler})"

    def __hash__(self) -> int:  # pyright: ignore[reportIncompatibleVariableOverride]
        return hash(self.id)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Subscription):
            return self.id == other.id
        return False

    @property
    def service_handler_obj(self) -> ServiceHandler:
        return get_service_handler_from_string(handler_string=self.service_handler)

    @property
    def subscription_handler_obj(self) -> SubscriptionHandler:
        return get_subscription_handler_from_string(handler_string=self.subscription_handler)

    @property
    def service(self) -> str:
        return self.service_handler_obj.TITLE

    @property
    def title(self) -> str:
        return self.subscription_handler_obj.TITLE

    @property
    def url(self) -> str:
        return self.subscription_handler_obj.URL


class SubscriptionCreate(SubscriptionBase):
    @root_validator(pre=True)
    @classmethod
    def set_pre_validation_defaults(cls, values: dict[str, Any]) -> dict[str, Any]:
        registered_service_handlers = get_registered_service_handlers()
        registered_subscription_handlers = get_registered_subscription_handlers()

        created_by = values["created_by"]
        service_handler = values["service_handler"]
        subscription_handler = values["subscription_handler"]

        if service_handler not in registered_service_handlers:
            raise ValueError("Service Handler '{}' is not valid".format(service_handler))

        if subscription_handler not in registered_subscription_handlers:
            raise ValueError("Subscription Handler '{}' is not valid".format(subscription_handler))

        subscription_id = generate_uuid_from_string(
            string=f"{service_handler}-{subscription_handler}-{created_by}"
        )
        return {
            **values,
            "id": subscription_id,
            "updated_at": datetime.datetime.now(tz=datetime.timezone.utc),
        }


class SubscriptionUpdate(SubscriptionBase):
    pass


class SubscriptionRead(SubscriptionBase):
    pass
