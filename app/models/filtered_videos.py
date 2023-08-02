from typing import TYPE_CHECKING

from sqlmodel import SQLModel

if TYPE_CHECKING:
    from app.models.criteria import Criteria
    from app.models.video import Video


class FilteredVideos(SQLModel):
    videos: list
    videos_limited_count: int
    videos_not_limited_count: int
    read_status: str
    show_hidden_channels: bool
    criterias: list
    ordered_by: str
    reverse_order: bool
    limit: int
