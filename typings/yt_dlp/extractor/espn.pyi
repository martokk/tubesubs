"""
This type stub file was generated by pyright.
"""

from .adobepass import AdobePassIE
from .common import InfoExtractor
from .once import OnceIE

class ESPNIE(OnceIE):
    _VALID_URL = ...
    _TESTS = ...


class ESPNArticleIE(InfoExtractor):
    _VALID_URL = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...



class FiveThirtyEightIE(InfoExtractor):
    _VALID_URL = ...
    _TEST = ...


class ESPNCricInfoIE(InfoExtractor):
    _VALID_URL = ...
    _TESTS = ...


class WatchESPNIE(AdobePassIE):
    _VALID_URL = ...
    _TESTS = ...
    _API_KEY = ...
