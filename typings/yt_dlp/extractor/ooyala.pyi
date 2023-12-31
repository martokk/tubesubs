"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class OoyalaBaseIE(InfoExtractor):
    _PLAYER_BASE = ...
    _CONTENT_TREE_BASE = ...
    _AUTHORIZATION_URL_TEMPLATE = ...


class OoyalaIE(OoyalaBaseIE):
    _VALID_URL = ...
    _TESTS = ...


class OoyalaExternalIE(OoyalaBaseIE):
    _VALID_URL = ...
    _TEST = ...
