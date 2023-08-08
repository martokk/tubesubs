from typing import TYPE_CHECKING, Any

from abc import abstractmethod
from urllib.parse import urlparse

from app.models.settings import Settings as _Settings
from app.services.ytdlp import YDL_OPTS_BASE, AwaitingTranscodingError, FormatNotFoundError

if TYPE_CHECKING:
    from app.models.video import Video

settings = _Settings()


class SubscriptionHandler:
    TITLE = "Base"
    SERVICE = ""
    COLOR = "#333333"
    URL = ""
    IS_SUBSCRIPTION_FEED = False  # if user is already subscribed to all channels

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def get_subscription_ydl_opts(
        self,
        playlistend: int = 100,
        playlistreverse: bool = False,
    ) -> dict[str, Any]:
        ...


class ServiceHandler:
    TITLE = "Base"
    DOMAINS: list[str] = []
    COLOR = "#333333"

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def sanitize_url(self, url: str) -> str:
        """
        Sanitizes the url to a standard format

        Args:
            url: The URL to be sanitized

        Returns:
            The sanitized URL.
        """
        parsed_url = urlparse(url)
        return parsed_url.geturl()

    def sanitize_video_url(self, url: str) -> str:
        """
        Sanitizes the Source url to a standard format

        Args:
            url: The URL to be sanitized

        Returns:
            The sanitized URL.
        """
        return self.sanitize_url(url=url)

    @abstractmethod
    def map_subscription_info_dict_entity_to_video_dict(
        self, subscription_id: str, entry_info_dict: dict[str, Any]
    ) -> dict[str, Any]:
        ...

    @abstractmethod
    def get_channel_ydl_opts(self) -> dict[str, Any]:
        ...

    @abstractmethod
    def get_channel_url(self, remote_channel_id: str) -> str:
        ...
