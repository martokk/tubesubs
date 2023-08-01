from sqlmodel import Field, SQLModel

from app.models.common import TimestampModel


class SubscriptionVideoLink(TimestampModel, SQLModel, table=True):
    subscription_id: str = Field(default=None, foreign_key="subscription.id", primary_key=True)
    video_id: str = Field(default=None, foreign_key="video.id", primary_key=True)
