"""
This type stub file was generated by pyright.
"""

from .common import PostProcessor

class SponSkrubPP(PostProcessor):
    _temp_ext = ...
    _exe_name = ...
    def __init__(self, downloader, path=..., args=..., ignoreerror=..., cut=..., force=..., _from_cli=...) -> None:
        ...

    def get_exe(self, path=...): # -> str | None:
        ...

    @PostProcessor._restrict_to(images=False)
    def run(self, information): # -> tuple[list[Unknown], Unknown]:
        ...
