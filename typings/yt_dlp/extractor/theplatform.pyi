"""
This type stub file was generated by pyright.
"""

from .once import OnceIE
from .adobepass import AdobePassIE

default_ns = ...
_x = ...
class ThePlatformBaseIE(OnceIE):
    _TP_TLD = ...


class ThePlatformIE(ThePlatformBaseIE, AdobePassIE):
    _VALID_URL = ...
    _EMBED_REGEX = ...
    _TESTS = ...


class ThePlatformFeedIE(ThePlatformBaseIE):
    _URL_TEMPLATE = ...
    _VALID_URL = ...
    _TESTS = ...
