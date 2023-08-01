from typing import Any

import datetime
import re

from app.models.settings import Settings as _Settings

from .base import ServiceHandler

settings = _Settings()


class YoutubeHandler(ServiceHandler):
    TITLE = "Youtube"
    DOMAINS = ["youtube.com"]
    COLOR = "#CC0000"

    def sanitize_video_url(self, url: str) -> str:
        """
        Sanitizes "/shorts" and "/watch" URLs to "/watch?v=" URL.

        Args:
            url: The URL to be sanitized

        Returns:
            The sanitized "/watch?v=" URL.
        """
        url = self.force_watch_v_format(url=url)
        return super().sanitize_video_url(url=url)

    def force_watch_v_format(self, url: str) -> str:
        """
        Extracts the YouTube video ID from a URL and returns the URL
        formatted like `https://www.youtube.com/watch?v=VIDEO_ID`.

        Args:
            url: The URL of the YouTube video.

        Returns:
            The formatted URL.

        Raises:
            ValueError: If the URL is not a valid YouTube video URL.
        """
        match = re.search(r"(?<=shorts/).*", url)
        if match:
            video_id = match.group()
        else:
            match = re.search(r"(?<=watch\?v=).*", url)
            if match:
                video_id = match.group()
            else:
                raise ValueError("Invalid YouTube video URL")

        return f"https://www.youtube.com/watch?v={video_id}"

    def map_subscription_info_dict_entity_to_video_dict(
        self, subscription_id: str, entry_info_dict: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Maps a video 'entry_info_dict' from a 'subscription_info_dict' to a `Video` object.
        Use this when when `extract_flat=True` is used.

        Args:
            source_id: The id of the source the video belongs to.
            entry_info_dict: A dictionary containing information about the video.

        Returns:
            A `Video` dictionary created from the `entry_info_dict`.
        """
        released_at = (
            datetime.datetime.strptime(entry_info_dict["upload_date"], "%Y%m%d").replace(
                tzinfo=datetime.timezone.utc
            )
            if entry_info_dict.get("upload_date")
            else None
        )
        url = entry_info_dict.get("webpage_url", entry_info_dict["url"])
        return {
            "subscription_id": subscription_id,
            "url": url,
            "added_at": datetime.datetime.now(tz=datetime.timezone.utc),
            "title": entry_info_dict["title"],
            "description": entry_info_dict["description"],
            "duration": entry_info_dict["duration"],
            "thumbnail": entry_info_dict["thumbnails"][-1]["url"],
            "released_at": released_at,
            "remote_video_id": entry_info_dict["id"],
            "remote_channel_id": entry_info_dict["channel_id"],
            "remote_channel_name": entry_info_dict["channel"],
        }

    def get_channel_ydl_opts(self) -> dict[str, Any]:
        return {
            "simulate": True,
            "silent": True,
            "skip_download": True,
            "extract_flat": True,
            "playliststart": 0,
            "playlistend": 0,
        }

    def get_channel_url(self, remote_channel_id: str) -> str:
        return f"https://www.youtube.com/channel/{remote_channel_id}"
