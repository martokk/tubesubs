"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class PalcoMP3BaseIE(InfoExtractor):
    _GQL_QUERY_TMPL = ...
    _ARTIST_FIELDS_TMPL = ...
    _MUSIC_FIELDS = ...


class PalcoMP3IE(PalcoMP3BaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...



class PalcoMP3ArtistIE(PalcoMP3BaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...
    _ARTIST_FIELDS_TMPL = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...



class PalcoMP3VideoIE(PalcoMP3BaseIE):
    IE_NAME = ...
    _VALID_URL = ...
    _TESTS = ...
    _MUSIC_FIELDS = ...
