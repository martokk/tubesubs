"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class BanByeBaseIE(InfoExtractor):
    _API_BASE = ...
    _CDN_BASE = ...
    _VIDEO_BASE = ...


class BanByeIE(BanByeBaseIE):
    _VALID_URL = ...
    _TESTS = ...


class BanByeChannelIE(BanByeBaseIE):
    _VALID_URL = ...
    _TESTS = ...
    _PAGE_SIZE = ...
