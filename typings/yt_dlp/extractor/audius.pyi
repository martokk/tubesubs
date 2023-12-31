"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class AudiusBaseIE(InfoExtractor):
    _API_BASE = ...
    _API_V = ...


class AudiusIE(AudiusBaseIE):
    _VALID_URL = ...
    IE_DESC = ...
    _TESTS = ...
    _ARTWORK_MAP = ...


class AudiusTrackIE(AudiusIE):
    _VALID_URL = ...
    IE_NAME = ...
    IE_DESC = ...
    _TESTS = ...


class AudiusPlaylistIE(AudiusBaseIE):
    _VALID_URL = ...
    IE_NAME = ...
    IE_DESC = ...
    _TEST = ...


class AudiusProfileIE(AudiusPlaylistIE):
    IE_NAME = ...
    IE_DESC = ...
    _VALID_URL = ...
    _TEST = ...
