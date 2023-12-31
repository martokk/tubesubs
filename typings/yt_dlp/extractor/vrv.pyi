"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class VRVBaseIE(InfoExtractor):
    _API_DOMAIN = ...
    _API_PARAMS = ...
    _CMS_SIGNING = ...
    _TOKEN = ...
    _TOKEN_SECRET = ...


class VRVIE(VRVBaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...
    _NETRC_MACHINE = ...


class VRVSeriesIE(VRVBaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TEST = ...
