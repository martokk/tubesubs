from app.models.criteria import Criteria, CriteriaField, CriteriaOperator, CriteriaUnitOfMeasure
from app.models.filter import Filter, FilterOrderedBy, FilterReadStatus
from app.models.filtered_videos import FilteredVideos
from app.models.subscription import Subscription
from app.models.video import Video


async def get_filtered_videos(filter_: "Filter", max_videos: int | None = None) -> FilteredVideos:
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
    videos = videos if not max_videos else await limit_videos(videos=videos, max_videos=max_videos)

    return FilteredVideos(
        filter=filter_,
        videos=videos,
        videos_limited_count=len(videos),
        videos_not_limited_count=videos_not_limited_count,
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

    # Filter by Tags
    videos = await filter_by_criteria_tags(videos=videos, criterias=criterias)

    return videos


async def filter_by_criteria_tags(videos: list[Video], criterias: list[Criteria]) -> list[Video]:
    """
    Filter videos based on criteria tags
    """
    criteria_must_contain_tags = [
        criteria.value
        for criteria in criterias
        if criteria.field == CriteriaField.CHANNEL.value
        and criteria.operator == CriteriaOperator.MUST_CONTAIN.value
    ]

    criteria_must_not_contain_tags = [
        criteria.value
        for criteria in criterias
        if criteria.field == CriteriaField.CHANNEL.value
        and criteria.operator == CriteriaOperator.MUST_NOT_CONTAIN.value
    ]

    criteria_duration = False
    criteria_duration_greater_than = 0
    criteria_duration_shorter_than = 86400
    for criteria in criterias:
        if criteria.field == CriteriaField.DURATION.value:
            criteria_duration = True

            # set value in seconds
            if criteria.unit_of_measure == CriteriaUnitOfMeasure.MINUTES.value:
                criteria_value_seconds = int(criteria.value) * 60
            elif criteria.unit_of_measure == CriteriaUnitOfMeasure.HOURS.value:
                criteria_value_seconds = int(criteria.value) * 60 * 60
            else:
                criteria_value_seconds = int(criteria.value)

            if criteria.operator == CriteriaOperator.LONGER_THAN.value:
                if criteria_value_seconds > criteria_duration_greater_than:
                    criteria_duration_greater_than = criteria_value_seconds

            if criteria.operator == CriteriaOperator.SHORTER_THAN.value:
                if criteria_value_seconds < criteria_duration_shorter_than:
                    criteria_duration_shorter_than = criteria_value_seconds

    if (
        not criteria_must_contain_tags
        and not criteria_must_not_contain_tags
        and not criteria_duration
    ):
        return videos

    # Filter Tags

    filtered_videos = []
    for video in videos:
        append_video = False
        video_channel_tags = [tag.name for tag in video.channel.tags]

        # Must Contain Tags
        if criteria_must_contain_tags:
            for video_channel_tag in video_channel_tags:
                if (
                    video_channel_tag in criteria_must_contain_tags
                    or "ANY" in criteria_must_contain_tags
                ):
                    append_video = True
                    break

        # Must NOT Contain Tags
        if criteria_must_not_contain_tags:
            for video_channel_tag in video_channel_tags:
                if video_channel_tag in criteria_must_not_contain_tags:
                    append_video = False
                    break
                else:
                    if "ANY" in criteria_must_not_contain_tags and len(video_channel_tags) > 0:
                        append_video = False
                        break
                    append_video = True

        # Duration
        if criteria_duration:
            if not video.duration:
                append_video = True
            else:
                if (
                    video.duration >= criteria_duration_greater_than
                    and video.duration <= criteria_duration_shorter_than
                ):
                    append_video = True
                else:
                    append_video = False

        # Append video
        if append_video:
            filtered_videos.append(video)

    return filtered_videos


async def sort_videos(
    videos: list[Video],
    ordered_by: str = FilterOrderedBy.CREATED_AT.value,
    reverse: bool = False,
) -> list[Video]:
    return sorted(videos, key=lambda video: getattr(video, ordered_by), reverse=reverse)


async def limit_videos(videos: list[Video], max_videos: int) -> list[Video]:
    return videos[:max_videos]
