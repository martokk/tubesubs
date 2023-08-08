from typing import Any

from sqlmodel import Session

from app import crud
from app.models import Subscription, VideoCreate
from app.models.channel import ChannelCreate, ChannelUpdate
from app.services.ytdlp import get_info_dict


async def get_subscription_info_dict(
    db_subscription: Subscription,
    reverse_import_order: bool = False,
    max_videos: int = 100,
) -> dict[str, Any]:
    """
    Retrieve the info_dict from yt-dlp for a Subscription

    Parameters:
        db_subscription: The Subscription object
        reverse_import_order (bool): Whether to reverse the order of the videos in the playlist.

    Returns:
        dict: The info dictionary for the Subscription

    """
    # Reverse they playlistreverse if reverse_import_order is True
    playlistreverse = reverse_import_order

    # Get ydl_opts from handler
    ydl_opts = db_subscription.subscription_handler_obj.get_subscription_ydl_opts(
        playlistend=max_videos, playlistreverse=playlistreverse
    )

    # Build subscription_info_dict
    _subscription_info_dict = await get_info_dict(
        url=db_subscription.url,
        ydl_opts=ydl_opts,
        # custom_extractors=custom_extractors,
        # ie_key="CustomRumbleChannel",
    )
    _subscription_info_dict["subscription_id"] = db_subscription.id

    return _subscription_info_dict


async def add_new_subscription_info_dict_videos_to_subscription(
    subscription_info_dict: dict[str, Any], db_subscription: Subscription, db: Session
) -> list[VideoCreate]:
    """
    Add new videos from a list of fetched videos to a Subscription in the database.

    Args:
        subscription_info_dict: the subscription_info_dict
        db_subscription: The Subscription object in the database to add the new videos to.
        db (Session): The database session.

    Returns:
        A list of Video objects that were added to the database.
    """

    # Check if is Subscription Feed (user is subscribed to all channels in feed)
    is_subscription_feed = db_subscription.subscription_handler_obj.IS_SUBSCRIPTION_FEED

    # Fetch Videos from Feed
    fetched_videos = get_subscription_videos_from_subscription_info_dict(
        subscription_info_dict=subscription_info_dict, db_subscription=db_subscription
    )
    db_video_ids = [video.id for video in db_subscription.videos]

    # Add videos that were fetched, but not in the database.
    new_videos = []
    for fetched_video in fetched_videos:
        if fetched_video.id not in db_video_ids:
            # Get Channel in Database
            db_channel = await crud.channel.get_or_none(
                db=db, remote_channel_id=fetched_video.remote_channel_id
            )

            # Create Channel if Needed
            if not db_channel:
                new_channel = ChannelCreate(
                    service_handler=db_subscription.service_handler,
                    remote_channel_id=fetched_video.remote_channel_id,
                    name=fetched_video.remote_channel_name,
                    is_subscribed=True if is_subscription_feed else False,
                )
                try:
                    db_channel = await crud.channel.create(obj_in=new_channel, db=db)
                except crud.RecordAlreadyExistsError:  # pragma: no cover
                    db_channel = await crud.channel.get(
                        db=db, remote_channel_id=new_channel.remote_channel_id
                    )

            # Check if channel is subscribed to
            if db_channel.is_subscribed is False and is_subscription_feed:
                channel_update = ChannelUpdate(is_subscribed=True)
                db_channel = await crud.channel.update(
                    db=db, id=db_channel.id, obj_in=channel_update
                )

            # Create Video in Database
            new_video = VideoCreate(**fetched_video.dict())
            new_videos.append(new_video)

            db_video = await crud.video.get_or_none(db=db, id=new_video.id)
            if not db_video:
                try:
                    db_video = await crud.video.create(obj_in=new_video, db=db)
                except crud.RecordAlreadyExistsError:  # pragma: no cover
                    db_video = await crud.video.get(db=db, id=new_video.id)  # pragma: no cover

            db_subscription.videos.append(db_video)

    return new_videos


def get_subscription_videos_from_subscription_info_dict(
    subscription_info_dict: dict[str, Any], db_subscription: Subscription
) -> list[VideoCreate]:
    """
    Get a list of `Video` objects from a subscription_info_dict.

    Parameters:
        subscription_info_dict (dict): The subscription_info_dict.
        db_subscription: The Subscription object

    Returns:
        list: The list of `Video` objects.
    """
    entries = subscription_info_dict["entries"]

    if len(entries) > 0 and entries[0]["_type"] == "playlist":
        playlists = entries
    else:
        playlists = [subscription_info_dict]

    video_dicts = []
    for playlist in playlists:
        for entry_info_dict in playlist.get("entries", []):
            if (
                not entry_info_dict.get("live_status")
                or entry_info_dict.get("live_status") == "was_live"
            ):
                if (
                    "[private video]" in str(entry_info_dict.get("title")).lower()
                    or "[deleted video]" in str(entry_info_dict.get("title")).lower()
                ):
                    continue
                service_handler = db_subscription.service_handler_obj
                video_dict = service_handler.map_subscription_info_dict_entity_to_video_dict(
                    subscription_id=db_subscription.id,
                    entry_info_dict=entry_info_dict,
                )
                video_dicts.append(video_dict)

    return [VideoCreate(**video_dict) for video_dict in video_dicts]
