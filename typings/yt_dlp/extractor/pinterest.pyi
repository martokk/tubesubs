"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class PinterestBaseIE(InfoExtractor):
    _VALID_URL_BASE = ...


class PinterestIE(PinterestBaseIE):
    _VALID_URL = ...
    _TESTS = ...


class PinterestCollectionIE(PinterestBaseIE):
    _VALID_URL = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...
