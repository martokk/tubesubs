from sqlmodel import Field, SQLModel

from app.models.common import TimestampModel


class ChannelTagLink(TimestampModel, SQLModel, table=True):
    channel_id: str | None = Field(default=None, foreign_key="channel.id", primary_key=True)
    tag_id: str | None = Field(default=None, foreign_key="tag.id", primary_key=True)
