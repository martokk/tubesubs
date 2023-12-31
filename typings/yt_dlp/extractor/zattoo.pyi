"""
This type stub file was generated by pyright.
"""

from .common import InfoExtractor

class ZattooPlatformBaseIE(InfoExtractor):
    _power_guide_hash = ...


class ZattooBaseIE(ZattooPlatformBaseIE):
    _NETRC_MACHINE = ...
    _HOST = ...


class ZattooIE(ZattooBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class ZattooLiveIE(ZattooBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...



class ZattooMoviesIE(ZattooBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class ZattooRecordingsIE(ZattooBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class NetPlusTVBaseIE(ZattooPlatformBaseIE):
    _NETRC_MACHINE = ...
    _HOST = ...
    _API_HOST = ...


class NetPlusTVIE(NetPlusTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class NetPlusTVLiveIE(NetPlusTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...



class NetPlusTVRecordingsIE(NetPlusTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class MNetTVBaseIE(ZattooPlatformBaseIE):
    _NETRC_MACHINE = ...
    _HOST = ...


class MNetTVIE(MNetTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class MNetTVLiveIE(MNetTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...



class MNetTVRecordingsIE(MNetTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class WalyTVBaseIE(ZattooPlatformBaseIE):
    _NETRC_MACHINE = ...
    _HOST = ...


class WalyTVIE(WalyTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class WalyTVLiveIE(WalyTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...



class WalyTVRecordingsIE(WalyTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class BBVTVBaseIE(ZattooPlatformBaseIE):
    _NETRC_MACHINE = ...
    _HOST = ...
    _API_HOST = ...


class BBVTVIE(BBVTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class BBVTVLiveIE(BBVTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...



class BBVTVRecordingsIE(BBVTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class VTXTVBaseIE(ZattooPlatformBaseIE):
    _NETRC_MACHINE = ...
    _HOST = ...
    _API_HOST = ...


class VTXTVIE(VTXTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class VTXTVLiveIE(VTXTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...



class VTXTVRecordingsIE(VTXTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class GlattvisionTVBaseIE(ZattooPlatformBaseIE):
    _NETRC_MACHINE = ...
    _HOST = ...


class GlattvisionTVIE(GlattvisionTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class GlattvisionTVLiveIE(GlattvisionTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...



class GlattvisionTVRecordingsIE(GlattvisionTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class SAKTVBaseIE(ZattooPlatformBaseIE):
    _NETRC_MACHINE = ...
    _HOST = ...
    _API_HOST = ...


class SAKTVIE(SAKTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class SAKTVLiveIE(SAKTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...



class SAKTVRecordingsIE(SAKTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class EWETVBaseIE(ZattooPlatformBaseIE):
    _NETRC_MACHINE = ...
    _HOST = ...


class EWETVIE(EWETVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class EWETVLiveIE(EWETVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...



class EWETVRecordingsIE(EWETVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class QuantumTVBaseIE(ZattooPlatformBaseIE):
    _NETRC_MACHINE = ...
    _HOST = ...
    _API_HOST = ...


class QuantumTVIE(QuantumTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class QuantumTVLiveIE(QuantumTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...



class QuantumTVRecordingsIE(QuantumTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class OsnatelTVBaseIE(ZattooPlatformBaseIE):
    _NETRC_MACHINE = ...
    _HOST = ...


class OsnatelTVIE(OsnatelTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class OsnatelTVLiveIE(OsnatelTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...



class OsnatelTVRecordingsIE(OsnatelTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class EinsUndEinsTVBaseIE(ZattooPlatformBaseIE):
    _NETRC_MACHINE = ...
    _HOST = ...
    _API_HOST = ...


class EinsUndEinsTVIE(EinsUndEinsTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class EinsUndEinsTVLiveIE(EinsUndEinsTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...



class EinsUndEinsTVRecordingsIE(EinsUndEinsTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class SaltTVBaseIE(ZattooPlatformBaseIE):
    _NETRC_MACHINE = ...
    _HOST = ...


class SaltTVIE(SaltTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...


class SaltTVLiveIE(SaltTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...
    @classmethod
    def suitable(cls, url): # -> bool:
        ...



class SaltTVRecordingsIE(SaltTVBaseIE):
    _VALID_URL = ...
    _TYPE = ...
    _TESTS = ...
