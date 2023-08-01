from sqlmodel import Field, SQLModel

from app.models.common import TimestampModel


class SubscriptionFilterLink(TimestampModel, SQLModel, table=True):
    subscription_id: str | None = Field(
        default=None, foreign_key="subscription.id", primary_key=True
    )
    filter_id: str | None = Field(default=None, foreign_key="filter.id", primary_key=True)
