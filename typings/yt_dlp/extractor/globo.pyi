"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class GloboIE(InfoExtractor):
    _VALID_URL = ...
    _NETRC_MACHINE = ...
    _TESTS = ...


class GloboArticleIE(InfoExtractor):
    _VALID_URL = ...
    _VIDEOID_REGEXES = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...
