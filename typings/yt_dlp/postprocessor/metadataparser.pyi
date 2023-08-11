"""
This type stub file was generated by pyright.
"""

from .common import PostProcessor
from ..utils import function_with_repr

class MetadataParserPP(PostProcessor):
    def __init__(self, downloader, actions) -> None:
        ...

    @classmethod
    def validate_action(cls, action, *data): # -> None:
        """Each action can be:
                (Actions.INTERPRET, from, to) OR
                (Actions.REPLACE, field, search, replace)
        """
        ...

    @staticmethod
    def field_to_template(tmpl): # -> str:
        ...

    @staticmethod
    def format_to_regex(fmt): # -> Literal['']:
        r"""
        Converts a string like
           '%(title)s - %(artist)s'
        to a regex like
           '(?P<title>.+)\ \-\ (?P<artist>.+)'
        """
        ...

    def run(self, info): # -> tuple[list[Unknown], Unknown]:
        ...

    @function_with_repr
    def interpretter(self, inp, out): # -> (info: Unknown) -> None:
        ...

    @function_with_repr
    def replacer(self, field, search, replace): # -> (info: Unknown) -> None:
        ...

    Actions = ...


class MetadataFromFieldPP(MetadataParserPP):
    @classmethod
    def to_action(cls, f): # -> tuple[Any, str | Any, str | Any]:
        ...

    def __init__(self, downloader, formats) -> None:
        ...



class MetadataFromTitlePP(MetadataParserPP):
    def __init__(self, downloader, titleformat) -> None:
        ...
