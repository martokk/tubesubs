"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class PlatziBaseIE(InfoExtractor):
    _LOGIN_URL = ...
    _NETRC_MACHINE = ...


class PlatziIE(PlatziBaseIE):
    _VALID_URL = ...
    _TESTS = ...


class PlatziCourseIE(PlatziBaseIE):
    _VALID_URL = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...
