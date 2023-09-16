from typing import Any

from sqlmodel import Session

from app import crud, logger
from app.models.channel import Channel, ChannelUpdate
from app.services.ytdlp import AccountNotFoundError, get_info_dict


async def check_and_update_null_channel_logos(db: Session) -> None:
    db_channels = await crud.channel.get_all(db=db)

    for db_channel in db_channels:
        if db_channel.logo:
            continue

        try:
            channel_logo = await get_channel_logo(db_channel=db_channel)
        except AccountNotFoundError as e:
            logger.error(e)
            await crud.channel.remove(db=db, id=db_channel.id)
            continue

        channel_update = ChannelUpdate(logo=channel_logo)
        await crud.channel.update(db=db, id=db_channel.id, obj_in=channel_update)


async def get_channel_logo(db_channel: Channel) -> str:
    channel_info_dict: dict[str, Any] = await get_channel_info_dict(db_channel=db_channel)

    full_size_logo = channel_info_dict["thumbnails"][-1]["url"].split("=")[0]
    small_logo = f"{full_size_logo}=s68-c-k-c0x00ffffff-no-rj"
    return str(small_logo)


async def get_channel_info_dict(db_channel: Channel) -> dict[str, Any]:
    """
    Retrieve the info_dict from yt-dlp for a channel

    Parameters:
        db_channel: The channel object

    Returns:
        dict: The info dictionary for the channel

    """
    ydl_opts = db_channel.service_handler_obj.get_channel_ydl_opts()
    info_dict: dict[str, Any] = await get_info_dict(
        url=db_channel.url,
        ydl_opts=ydl_opts,
    )
    return info_dict
