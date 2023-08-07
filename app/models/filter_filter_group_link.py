from sqlmodel import Field, SQLModel

from app.models.common import TimestampModel


class FilterFilterGroupLink(TimestampModel, SQLModel, table=True):
    filter_id: str = Field(default=None, foreign_key="filter.id", primary_key=True)
    filter_group_id: str = Field(default=None, foreign_key="filtergroup.id", primary_key=True)
