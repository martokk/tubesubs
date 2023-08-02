from app.models.criteria import (
    Criteria,
    CriteriaField,
    CriteriaOperator,
    CriteriaUnitOfMeasure,
    CriteriaValue,
)
from app.models.filter import Filter, FilterOrderedBy, FilterReadStatus
from app.models.subscription import Subscription
from app.models.video import Video
from app.models.filtered_videos import FilteredVideos


async def get_filtered_videos(filter_: "Filter", max_videos: int) -> FilteredVideos:
    """
    Filter videos based on the filter criteria.
    """
    # Get videos
    videos = await get_videos_from_subscriptions(subscriptions=filter_.subscriptions)

    # Filter By Read Status
    videos = await filter_by_read_status(videos=videos, read_status=filter_.read_status)

    # Filter Hidden Channels
    videos = await filter_hidden_channels(videos=videos)

    # Filter By Criterias
    videos = await filter_by_criterias(videos=videos, criterias=filter_.criterias)

    # Sort videos by Ordered By attribute
    videos = await sort_videos(
        videos=videos, ordered_by=filter_.ordered_by, reverse=filter_.reverse_order
    )

    # Limit Videos
    videos_not_limited_count = len(videos)
    videos = await limit_videos(videos=videos, max_videos=max_videos)

    return FilteredVideos(
        videos=videos,
        videos_limited_count=len(videos),
        videos_not_limited_count=videos_not_limited_count,
        read_status=filter_.read_status,
        show_hidden_channels=filter_.show_hidden_channels,
        criterias=filter_.criterias,
        ordered_by=filter_.ordered_by,
        reverse_order=filter_.reverse_order,
        limit=max_videos,
    )


async def get_videos_from_subscriptions(subscriptions: list[Subscription]) -> list[Video]:
    """
    Get all videos from subscriptions
    """
    videos = []
    for subscription in subscriptions:
        videos.extend(subscription.videos)
    return videos


async def filter_by_read_status(videos: list[Video], read_status: str) -> list[Video]:
    """
    Filter videos based on the read status.
    """
    if read_status == FilterReadStatus.READ.value:
        return [video for video in videos if video.is_read is True]
    if read_status == FilterReadStatus.UNREAD.value:
        return [video for video in videos if video.is_read is False]
    return videos


async def filter_hidden_channels(videos: list[Video]) -> list[Video]:
    """
    Filter videos based on the hidden channels.
    """
    return [video for video in videos if video.channel.is_hidden is False]


async def filter_by_criterias(videos: list[Video], criterias: list[Criteria]) -> list[Video]:
    """
    Filter videos based on all filter criterias
    """

    return videos


async def sort_videos(
    videos: list[Video],
    ordered_by: str = FilterOrderedBy.CREATED_AT.value,
    reverse: bool = False,
) -> list[Video]:
    return sorted(videos, key=lambda video: getattr(video, ordered_by), reverse=reverse)


async def limit_videos(videos: list[Video], max_videos: int) -> list[Video]:
    return videos[:max_videos]
