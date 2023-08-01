from urllib.parse import ParseResult, urlparse

from app.handlers.exceptions import HandlerNotFoundError

from .base import ServiceHandler, SubscriptionHandler
from .rumble import RumbleHandler
from .youtube import YoutubeHandler
from .youtube_subscription import YoutubeSubscriptionHandler

registered_service_handlers = [YoutubeHandler()]
registered_subscription_handlers = [YoutubeSubscriptionHandler()]


def get_registered_service_handlers() -> list[str]:
    return [handler.name for handler in registered_service_handlers]


def get_registered_subscription_handlers() -> list[str]:
    return [handler.name for handler in registered_subscription_handlers]


def get_registered_service_handlers_titles() -> list[str]:
    return [handler.TITLE for handler in registered_service_handlers]


def get_registered_subscription_handlers_titles() -> list[str]:
    return [handler.TITLE for handler in registered_subscription_handlers]


def get_service_handler_from_url(url: str | ParseResult) -> ServiceHandler:
    url = url if isinstance(url, ParseResult) else urlparse(url=url)
    domain_name = ".".join(url.netloc.split(".")[-2:])

    if domain_name in YoutubeHandler.DOMAINS:
        return YoutubeHandler()
    if domain_name in RumbleHandler.DOMAINS:
        return RumbleHandler()
    raise HandlerNotFoundError(f"A handler could not be found for url: `{str(url)}`.")


def get_service_handler_from_string(handler_string: str) -> ServiceHandler:
    if handler_string == "YoutubeHandler" or handler_string == "Youtube":
        return YoutubeHandler()
    if handler_string == "RumbleHandler" or handler_string == "Rumble":
        return RumbleHandler()
    raise HandlerNotFoundError(f"A handler could not be found for {handler_string=}.")


def get_subscription_handler_from_string(handler_string: str) -> SubscriptionHandler:
    if handler_string == "YoutubeSubscriptionHandler" or handler_string == "YoutubeSubscription":
        return YoutubeSubscriptionHandler()
    raise HandlerNotFoundError(f"A handler could not be found for {handler_string=}.")
