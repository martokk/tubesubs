"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class TV5UnisBaseIE(InfoExtractor):
    _GEO_COUNTRIES = ...


class TV5UnisVideoIE(TV5UnisBaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TEST = ...
    _GQL_QUERY_NAME = ...


class TV5UnisIE(TV5UnisBaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...
    _GQL_QUERY_NAME = ...
