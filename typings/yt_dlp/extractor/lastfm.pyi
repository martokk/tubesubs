"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class LastFMPlaylistBaseIE(InfoExtractor):
    ...


class LastFMPlaylistIE(LastFMPlaylistBaseIE):
    _VALID_URL = ...
    _TESTS = ...


class LastFMUserIE(LastFMPlaylistBaseIE):
    _VALID_URL = ...
    _TESTS = ...


class LastFMIE(InfoExtractor):
    _VALID_URL = ...
    _TESTS = ...
