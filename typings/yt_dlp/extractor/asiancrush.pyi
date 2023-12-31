"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class AsianCrushBaseIE(InfoExtractor):
    _VALID_URL_BASE = ...
    _KALTURA_KEYS = ...
    _API_SUFFIX = ...


class AsianCrushIE(AsianCrushBaseIE):
    _VALID_URL = ...
    _TESTS = ...


class AsianCrushPlaylistIE(AsianCrushBaseIE):
    _VALID_URL = ...
    _TESTS = ...
    _PAGE_SIZE = ...
