from sqlmodel import SQLModel


class FilteredVideos(SQLModel):
    videos: list  # type: ignore
    videos_limited_count: int
    videos_not_limited_count: int
    read_status: str
    show_hidden_channels: bool
    criterias: list  # type: ignore
    reverse_order: bool
    limit: int
