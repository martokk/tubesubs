from typing import TYPE_CHECKING, Any

from app import paths
from app.handlers.base import SubscriptionHandler
from app.handlers.youtube import YoutubeHandler
from app.models.settings import Settings as _Settings
from app.services.ytdlp import get_info_dict

if TYPE_CHECKING:
    from app.models.video import Video

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
            # "outtmpl": '%(id)s',
            "playliststart": 0,
            "playlistend": playlistend,
        }
