from typing import Any, Type

from loguru import logger as _logger
from yt_dlp import YoutubeDL
from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import DownloadError, ExtractorError, YoutubeDLError

# from app.core.loggers import ytdlp_logger as logger
from app.core.notify import notify

# YoutubeDL Logger
logger = _logger.bind(name="logger")
ytdlp_logger = _logger.bind(name="ytdlp_logger")

# YoutubeDL Base Options
YDL_OPTS_BASE: dict[str, Any] = {
    "format": "worst[ext=mp4]",
    "skip_download": True,
    "simulate": True,
    "no_color": True,
    "ignore_no_formats_error": False,  # Ignore "No video formats" error. Extracts metadata if no formats are available.
    # "verbose": True,
}


class IsLiveEventError(YoutubeDLError):
    """
    Raised when a video is a live event.
    """


class Http410Error(YoutubeDLError):
    """
    Raised after a HTTP 410 "GONE" error.
    """


class IsPrivateVideoError(YoutubeDLError):
    """
    Raised when a video is private.
    """


class IsDeletedVideoError(YoutubeDLError):
    """
    Raised when a video is deleted.
    """


class PlaylistNotFoundError(YoutubeDLError):
    """
    Raised when a playlist does not exist.
    """


class NoUploadsError(YoutubeDLError):
    """
    Raised when a channel has no uploads.
    """


class AccountNotFoundError(YoutubeDLError):
    """
    Raised when a channel has been terminated or deleted.
    """


class VideoUnavailableError(YoutubeDLError):
    """
    Raised when a video is unavailable.
    """


class FormatNotFoundError(Exception):
    """
    Exception raised when a format cannot be found.
    """


class AwaitingTranscodingError(Exception):
    """
    Exception raised when a video is awaiting transcoding.
    """


async def get_info_dict(
    url: str,
    ydl_opts: dict[str, Any],
    ie_key: str | None = None,
    custom_extractors: list[Type[InfoExtractor]] | None = None,
) -> dict[str, Any]:
    """
    Use YouTube-DL to get the info dictionary for a given URL.

    Parameters:
        url (str): The URL of the object to retrieve info for.
        ydl_opts (dict[str, Any]): The options to use with YouTube-DL.
        ie_key (Optional[str]): The name of the YouTube-DL info extractor to use.
            If not provided, the default extractor will be used.
        custom_extractors (Optional[list[Type[InfoExtractor]]]): A list of
            Custom Extractors to make available to yt-dlp.

    Returns:
        dict[str, Any]: The info dictionary for the object.
    """
    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Extract info dict, handle if no videos uploaded
            info_dict = await get_info_dict_from_ydl(
                ydl=ydl,
                url=url,
                ydl_opts=ydl_opts,
                ie_key=ie_key,
                custom_extractors=custom_extractors,
            )
    except NoUploadsError as e:
        # TODO: Handle this error.
        # Test: https://www.youtube.com/channel/UCeTX6IZlqeB6qhNBAB6cgTQ
        # See: https://github.com/yt-dlp/yt-dlp/issues/5906
        raise e
    return info_dict


async def get_info_dict_from_ydl(
    ydl: YoutubeDL,
    url: str,
    ydl_opts: dict[str, Any],
    ie_key: str | None = None,
    custom_extractors: list[Type[InfoExtractor]] | None = None,
) -> dict[str, Any]:
    """
    Use YouTube-DL to get the info dictionary for a given URL.

    Parameters:
        ydl (YoutubeDL): The YouTube-DL instance to use.
        url (str): The URL of the object to retrieve info for.
        ydl_opts (dict[str, Any]): The options to use with YouTube-DL.
        ie_key (Optional[str]): The name of the YouTube-DL info extractor to use.
            If not provided, the default extractor will be used.
        custom_extractors (Optional[list[Type[InfoExtractor]]]): A list of
            Custom Extractors to make available to yt-dlp.

    Returns:
        dict[str, Any]: The info dictionary for the object.
    """
    # Add custom_extractors
    if custom_extractors:
        for custom_extractor in custom_extractors:
            ydl.add_info_extractor(custom_extractor())

    # Extract info dict, handle if no videos uploaded
    info_dict = await ydl_extract_info(ydl=ydl, url=url, download=False, ie_key=ie_key)

    # Append Metadata to info_dict
    info_dict["metadata"] = {
        "url": url,
        "ydl_opts": ydl_opts,
        "ie_key": ie_key,
        "custom_extractors": custom_extractors,
    }
    return info_dict


async def ydl_extract_info(
    ydl: YoutubeDL, url: str, ie_key: str | None, download: bool = False
) -> dict[str, Any]:
    """
    Use YouTube-DL to extract info for a given URL.

    Parameters:
        ydl (YoutubeDL): The YouTube-DL object to use.
        url (str): The URL of the object to retrieve info for.
        download (bool): Whether to download the video or not. Defaults to False.
        ie_key (Optional[str]): The name of the YouTube-DL info extractor to use.

    Returns:
        dict[str, Any]: The info dictionary for the object.

    Raises:
        IsLiveEventError: If the video is a live event.
        IsPrivateVideoError: If the video is private.
        YoutubeDLError: If the info dictionary could not be retrieved.
        YoutubeDLError: If the info dictionary is None.
        Http410Error: If a HTTP 410 "GONE" error is encountered.
    """
    try:
        info_dict: dict[str, Any] | None = ydl.extract_info(
            url, download=download, ie_key=ie_key, process=True
        )
    except (YoutubeDLError, DownloadError, ExtractorError) as e:
        if "This account has been terminated" in str(e):
            try:
                error_msg = e.exc_info[1].orig_msg  # type: ignore
            except AttributeError:
                error_msg = "This account has been terminated."
            raise AccountNotFoundError(str(error_msg)) from e
        if "Video unavailable" in str(e):
            raise VideoUnavailableError(str(e)) from e
        if "This channel has no uploads" in str(e):
            raise NoUploadsError("This channel has no uploads.") from e
        if "The playlist does not exist." in str(e):
            raise PlaylistNotFoundError("The playlist does not exist.") from e
        if "No video formats found" in str(e):
            raise IsLiveEventError("No video formats found.") from e
        if "this live event will begin in" in str(e):
            raise IsLiveEventError("This video is a live event.") from e
        if "[Private video]" in str(e):
            raise IsPrivateVideoError("This video is a private video.") from e
        if "[Deleted video]" in str(e):
            raise IsDeletedVideoError("This video is a deleted video.") from e
        if "Requested format is not available." in str(e):
            raise FormatNotFoundError(e) from e
        if "Internal Server Error" in str(e):
            raise VideoUnavailableError(e) from e
        if e.__class__.__name__ == "DownloadError":
            if "HTTP Error 410" in str(e):
                raise Http410Error from e

        err_msg = f"yt-dlp could not extract info for {url}. {e=}"
        logger.critical(err_msg)
        ytdlp_logger.critical(err_msg)
        await notify(telegram=True, email=False, text=err_msg)
        raise YoutubeDLError(err_msg) from e

    # Handle if info_dict is None/Empty
    if info_dict is None:
        raise YoutubeDLError(
            f"yt-dlp did not download a info_dict object. {info_dict=} {url=} {ie_key=} {ydl=}"
        )

    # Handle if video is a live event
    if info_dict.get("is_live"):
        raise IsLiveEventError("This video is a live event.")

    return info_dict
