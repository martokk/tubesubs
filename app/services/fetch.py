from sqlmodel import Session

from app import crud, logger
from app.models import FetchResults
from app.services.channel import check_and_update_null_channel_logos

# from app.services.feed import build_subscription_rss_files
from app.services.subscription import (
    add_new_subscription_info_dict_videos_to_subscription,
    get_subscription_info_dict,
)
from app.services.ytdlp import NoUploadsError


class FetchError(Exception):
    """
    Base class for fetch errors.
    """


class FetchCanceledError(FetchError):
    """
    Raised when a fetch is cancelled.
    """


async def fetch_subscription(
    db: Session, id: str, ignore_video_refresh: bool = False
) -> FetchResults:
    """
    Fetch new data from yt-dlp for the subscription and update the subscription in the database.

    Args:
        db (Session): The database session.
        id: The id of the subscription to fetch and update.

    Returns:
        models.FetchResult: The result of the fetch.
    """

    db_subscription = await crud.subscription.get(id=id, db=db)

    info_message = f"Fetching {db_subscription.__repr__()}"
    logger.info(info_message)

    # Fetch subscription information from yt-dlp and create the subscription object
    try:
        subscription_info_dict = await get_subscription_info_dict(
            db_subscription=db_subscription, reverse_import_order=True, max_videos=400
        )
    except (NoUploadsError, Exception) as e:
        raise FetchCanceledError from e

    # Use subscription_info_dict to add new videos to the subscription
    new_videos = await add_new_subscription_info_dict_videos_to_subscription(
        db=db, subscription_info_dict=subscription_info_dict, db_subscription=db_subscription
    )

    # Check channels for missing logos
    await check_and_update_null_channel_logos(db=db)

    # Build RSS Files
    # await build_subscription_rss_files(subscription=db_subscription)

    success_message = (
        f"Completed fetching {db_subscription.__repr__()}. Added {len(new_videos)} new videos. "
    )
    logger.success(success_message)

    return FetchResults(
        subscriptions=1,
        added_videos=len(new_videos),
        deleted_videos=0,
    )
