"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class GameJoltBaseIE(InfoExtractor):
    _API_BASE = ...


class GameJoltIE(GameJoltBaseIE):
    _VALID_URL = ...
    _TESTS = ...


class GameJoltPostListBaseIE(GameJoltBaseIE):
    ...


class GameJoltUserIE(GameJoltPostListBaseIE):
    _VALID_URL = ...
    _TESTS = ...


class GameJoltGameIE(GameJoltPostListBaseIE):
    _VALID_URL = ...
    _TESTS = ...


class GameJoltGameSoundtrackIE(GameJoltBaseIE):
    _VALID_URL = ...
    _TESTS = ...


class GameJoltCommunityIE(GameJoltPostListBaseIE):
    _VALID_URL = ...
    _TESTS = ...


class GameJoltSearchIE(GameJoltPostListBaseIE):
    _VALID_URL = ...
    _URL_FORMATS = ...
    _TESTS = ...
