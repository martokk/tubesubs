"""
This type stub file was generated by pyright.
"""

from .common import PostProcessor

class MoveFilesAfterDownloadPP(PostProcessor):
    def __init__(self, downloader=..., downloaded=...) -> None:
        ...

    @classmethod
    def pp_key(cls): # -> Literal['MoveFiles']:
        ...

    def run(self, info): # -> tuple[list[Unknown], Unknown]:
        ...
