"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class Ant1NewsGrBaseIE(InfoExtractor):
    ...


class Ant1NewsGrWatchIE(Ant1NewsGrBaseIE):
    IE_NAME = ...
    IE_DESC = ...
    _VALID_URL = ...
    _API_PATH = ...
    _TESTS = ...


class Ant1NewsGrArticleIE(Ant1NewsGrBaseIE):
    IE_NAME = ...
    IE_DESC = ...
    _VALID_URL = ...
    _TESTS = ...


class Ant1NewsGrEmbedIE(Ant1NewsGrBaseIE):
    IE_NAME = ...
    IE_DESC = ...
    _BASE_PLAYER_URL_RE = ...
    _VALID_URL = ...
    _EMBED_REGEX = ...
    _API_PATH = ...
    _TESTS = ...
