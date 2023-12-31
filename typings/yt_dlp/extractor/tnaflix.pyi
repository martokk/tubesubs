"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class TNAFlixNetworkBaseIE(InfoExtractor):
    _CONFIG_REGEX = ...
    _TITLE_REGEX = ...
    _DESCRIPTION_REGEX = ...
    _UPLOADER_REGEX = ...
    _VIEW_COUNT_REGEX = ...
    _COMMENT_COUNT_REGEX = ...
    _AVERAGE_RATING_REGEX = ...
    _CATEGORIES_REGEX = ...


class TNAFlixNetworkEmbedIE(TNAFlixNetworkBaseIE):
    _VALID_URL = ...
    _EMBED_REGEX = ...
    _TESTS = ...


class TNAEMPFlixBaseIE(TNAFlixNetworkBaseIE):
    _DESCRIPTION_REGEX = ...
    _UPLOADER_REGEX = ...
    _CATEGORIES_REGEX = ...


class TNAFlixIE(TNAEMPFlixBaseIE):
    _VALID_URL = ...
    _TITLE_REGEX = ...
    _TESTS = ...


class EMPFlixIE(TNAEMPFlixBaseIE):
    _VALID_URL = ...
    _TESTS = ...


class MovieFapIE(TNAFlixNetworkBaseIE):
    _VALID_URL = ...
    _VIEW_COUNT_REGEX = ...
    _COMMENT_COUNT_REGEX = ...
    _AVERAGE_RATING_REGEX = ...
    _CATEGORIES_REGEX = ...
    _TESTS = ...
