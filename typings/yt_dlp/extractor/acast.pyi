"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class ACastBaseIE(InfoExtractor):
    ...


class ACastIE(ACastBaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...


class ACastChannelIE(ACastBaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...
