"""
This type stub file was generated by pyright.
"""

"""
A partial parser for WebVTT segments. Interprets enough of the WebVTT stream
to be able to assemble a single stand-alone subtitle file, suitably adjusting
timestamps on the way, while everything else is passed through unmodified.

Regular expressions based on the W3C WebVTT specification
<https://www.w3.org/TR/webvtt1/>. The X-TIMESTAMP-MAP extension is described
in RFC 8216 §3.5 <https://tools.ietf.org/html/rfc8216#section-3.5>.
"""
class _MatchParser:
    """
    An object that maintains the current parsing position and allows
    conveniently advancing it as syntax elements are successfully parsed.
    """
    def __init__(self, string) -> None:
        ...

    def match(self, r): # -> Match[str] | int | None:
        ...

    def advance(self, by): # -> Match[Unknown] | str | int:
        ...

    def consume(self, r): # -> Match[str] | <subclass of int and str> | int | None:
        ...

    def child(self): # -> _MatchChildParser:
        ...



class _MatchChildParser(_MatchParser):
    """
    A child parser state, which advances through the same data as
    its parent, but has an independent position. This is useful when
    advancing through syntax elements we might later want to backtrack
    from.
    """
    def __init__(self, parent) -> None:
        ...

    def commit(self): # -> Unknown:
        """
        Advance the parent state to the current position of this child state.
        """
        ...



class ParseError(Exception):
    def __init__(self, parser) -> None:
        ...



_REGEX_TS = ...
_REGEX_EOF = ...
_REGEX_NL = ...
_REGEX_BLANK = ...
class Block:
    """
    An abstract WebVTT block.
    """
    def __init__(self, **kwargs) -> None:
        ...

    @classmethod
    def parse(cls, parser): # -> Self@Block | None:
        ...

    def write_into(self, stream): # -> None:
        ...



class HeaderBlock(Block):
    """
    A WebVTT block that may only appear in the header part of the file,
    i.e. before any cue blocks.
    """
    ...


class Magic(HeaderBlock):
    _REGEX = ...
    _REGEX_TSMAP = ...
    _REGEX_TSMAP_LOCAL = ...
    _REGEX_TSMAP_MPEGTS = ...
    _REGEX_TSMAP_SEP = ...
    _REGEX_META = ...
    @classmethod
    def parse(cls, parser): # -> Self@Magic:
        ...

    def write_into(self, stream): # -> None:
        ...



class StyleBlock(HeaderBlock):
    _REGEX = ...


class RegionBlock(HeaderBlock):
    _REGEX = ...


class CommentBlock(Block):
    _REGEX = ...


class CueBlock(Block):
    """
    A cue block. The payload is not interpreted.
    """
    _REGEX_ID = ...
    _REGEX_ARROW = ...
    _REGEX_SETTINGS = ...
    _REGEX_PAYLOAD = ...
    @classmethod
    def parse(cls, parser): # -> Self@CueBlock | None:
        ...

    def write_into(self, stream): # -> None:
        ...

    @property
    def as_json(self): # -> dict[str, Unknown]:
        ...

    def __eq__(self, other) -> bool:
        ...

    @classmethod
    def from_json(cls, json): # -> Self@CueBlock:
        ...

    def hinges(self, other): # -> Literal[False]:
        ...



def parse_fragment(frag_content): # -> Generator[Magic | RegionBlock | StyleBlock | CommentBlock | CueBlock, Any, None]:
    """
    A generator that yields (partially) parsed WebVTT blocks when given
    a bytes object containing the raw contents of a WebVTT file.
    """
    ...
