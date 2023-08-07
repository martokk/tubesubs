from typing import TYPE_CHECKING, Any

import json

from pydantic import root_validator
from sqlmodel import Field, Relationship, SQLModel

from app import models
from app.core.uuid import generate_uuid_random

from .common import TimestampModel

if TYPE_CHECKING:
    from .filter import Filter  # pragma: no cover


class FilterGroupBase(TimestampModel, SQLModel):
    id: str = Field(default=None, primary_key=True, index=True)
    name: str = Field(default=None)
    ordered_filter_ids_str: str = Field(default=None)


class FilterGroup(FilterGroupBase, table=True):
    filters: list["Filter"] = Relationship(
        back_populates="filter_groups",
        link_model=models.FilterFilterGroupLink,
    )

    @property
    def ordered_filter_ids(self):
        return json.loads(self.ordered_filter_ids_str)

    @property
    def ordered_filters(self):
        # Sort filters based on the order of filter ids in order_of_filter_ids
        try:
            return sorted(self.filters, key=lambda f: self.ordered_filter_ids.index(f.id))
        except ValueError as e:
            print(e)
            return self.filters


class FilterGroupCreate(FilterGroupBase, TimestampModel):
    @root_validator(pre=True)
    @classmethod
    def set_pre_validation_defaults(cls, values: dict[str, Any]) -> dict[str, Any]:
        filter_group_id = generate_uuid_random()
        return {
            **values,
            "id": filter_group_id,
        }


class FilterGroupUpdate(FilterGroupBase):
    ...


class FilterGroupRead(FilterGroupBase):
    ...
