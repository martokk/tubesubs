"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class PixivSketchBaseIE(InfoExtractor):
    ...


class PixivSketchIE(PixivSketchBaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...


class PixivSketchUserIE(PixivSketchBaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...
