"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor, SearchInfoExtractor

class NetverseBaseIE(InfoExtractor):
    _ENDPOINTS = ...


class NetverseIE(NetverseBaseIE):
    _VALID_URL = ...
    _TESTS = ...


class NetversePlaylistIE(NetverseBaseIE):
    _VALID_URL = ...
    _TESTS = ...
    def parse_playlist(self, json_data, playlist_id): # -> Generator[dict[str, str], Any, None]:
        ...



class NetverseSearchIE(SearchInfoExtractor):
    _SEARCH_KEY = ...
    _TESTS = ...