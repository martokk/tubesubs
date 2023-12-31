"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class SkyItPlayerIE(InfoExtractor):
    IE_NAME = ...
    _VALID_URL = ...
    _GEO_BYPASS = ...
    _DOMAIN = ...
    _PLAYER_TMPL = ...
    _TOKEN_MAP = ...


class SkyItVideoIE(SkyItPlayerIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...


class SkyItVideoLiveIE(SkyItPlayerIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TEST = ...


class SkyItIE(SkyItPlayerIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...
    _VIDEO_ID_REGEX = ...


class SkyItArteIE(SkyItIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...
    _DOMAIN = ...
    _VIDEO_ID_REGEX = ...


class CieloTVItIE(SkyItIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...
    _DOMAIN = ...
    _VIDEO_ID_REGEX = ...


class TV8ItIE(SkyItVideoIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...
    _DOMAIN = ...
