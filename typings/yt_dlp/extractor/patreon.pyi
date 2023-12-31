"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class PatreonBaseIE(InfoExtractor):
    USER_AGENT = ...


class PatreonIE(PatreonBaseIE):
    _VALID_URL = ...
    _TESTS = ...


class PatreonCampaignIE(PatreonBaseIE):
    _VALID_URL = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...
