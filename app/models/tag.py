from typing import TYPE_CHECKING, Any

from pydantic import root_validator
from sqlmodel import Field, Relationship, SQLModel

from app.core.uuid import generate_uuid_from_string
from app.models.channel_tag_link import ChannelTagLink
from app.services.color_hex import get_color_from_string

from .common import TimestampModel

if TYPE_CHECKING:
    from .channel import Channel  # pragma: no cover


class TagBase(TimestampModel, SQLModel):
    id: str = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(default=None)
    color: str = Field(default=None)


class Tag(TagBase, table=True):
    channels: list["Channel"] = Relationship(
        back_populates="tags",
        link_model=ChannelTagLink,
    )

    def __repr__(self) -> str:
        return f"Tag(id={self.id}, name={self.name if self.name else ''}"

    def __hash__(self) -> int:  # pyright: ignore[reportIncompatibleVariableOverride]
        return hash(self.id)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Tag):
            return self.id == other.id
        return False


class TagCreate(TagBase):
    @root_validator(pre=True)
    @classmethod
    def set_pre_validation_defaults(cls, values: dict[str, Any]) -> dict[str, Any]:
        name = values["name"].lower()
        tag_id = generate_uuid_from_string(string=name)
        color = values.get("color", get_color_from_string(string=name))
        return {
            **values,
            "id": tag_id,
            "name": name,
            "color": color,
        }


class TagUpdate(TagBase):
    pass


class TagRead(TagBase):
    pass
