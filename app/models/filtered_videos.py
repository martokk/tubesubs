from sqlmodel import SQLModel

from app.models.filter import Filter


class FilteredVideos(SQLModel):
    filter: Filter | None = None
    videos: list = []  # type: ignore
    videos_limited_count: int = 0
    videos_not_limited_count: int = 0
    limit: int | None = None
