from typing import Any

import datetime

from loguru import logger as _logger

from app.models.settings import Settings as _Settings
from app.paths import LOG_FILE as _LOG_FILE
from app.services.ytdlp import YDL_OPTS_BASE, AwaitingTranscodingError, FormatNotFoundError

from .base import ServiceHandler

settings = _Settings()

# Main Logger
logger = _logger.bind(name="logger")
logger.add(_LOG_FILE, level="WARNING", rotation="10 MB")


class RumbleHandler(ServiceHandler):
    TITLE = "Rumble"
    DOMAINS = ["rumble.com"]
    COLOR = "#85c742"

    def get_video_ydl_opts(self) -> dict[str, Any]:
        """
        Get the yt-dlp options for a video.

        Returns:
            dict: The yt-dlp options for the source.
        """
        return {
            **YDL_OPTS_BASE,
            # "allowed_extractors": self.YDL_OPT_ALLOWED_EXTRACTORS,
        }

    def map_subscription_info_dict_entity_to_video_dict(
        self, subscription_id: str, entry_info_dict: dict[str, Any]
    ) -> dict[str, Any]:
        # TODO: RumbleHandler - NotImplemented
        return {}

    def get_channel_ydl_opts(self) -> dict[str, Any]:
        # TODO: RumbleHandler - NotImplemented
        return {}

    def get_channel_url(self, remote_channel_id: str) -> str:
        # TODO: RumbleHandler - NotImplemented
        return ""
