"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class CybraryBaseIE(InfoExtractor):
    _API_KEY = ...
    _ENDPOINTS = ...
    _NETRC_MACHINE = ...
    _TOKEN = ...


class CybraryIE(CybraryBaseIE):
    _VALID_URL = ...
    _TESTS = ...


class CybraryCourseIE(CybraryBaseIE):
    _VALID_URL = ...
    _TESTS = ...
