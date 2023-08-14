from typing import Any

import yt_dlp

from app import paths
from app.handlers.base import SubscriptionHandler
from app.models.settings import Settings as _Settings

settings = _Settings()


class YoutubeRecommendedHandler(SubscriptionHandler):
    TITLE = "Youtube Recommended"
    SERVICE = "YoutubeHandler"
    COLOR = "#333333"
    URL = "https://www.youtube.com/feed/recommended"
    COOKIES_FILE = paths.YOUTUBE_COOKIES_FILE
    IS_SUBSCRIPTION_FEED = False  # if user is already subscribed to all channels

    def get_subscription_ydl_opts(
        self,
        playlistend: int = 100,
        playlistreverse: bool = False,
    ) -> dict[str, Any]:
        """
        Get the yt-dlp options for a subscription.

        Parameters:
            playlistend (int): The index of the last video to extract.

        Returns:
            dict: The yt-dlp options for the source.
        """
        return {
            "cookiefile": self.COOKIES_FILE,
            "simulate": True,
            "silent": True,
            "skip_download": True,
            "extract_flat": True,
            "no_warnings": True,
            "playlistreverse": playlistreverse,
            "playliststart": 0,
            "playlistend": playlistend,
            "match_filter": yt_dlp.utils.match_filter_func("duration < 3600"),
        }
