"""
This type stub file was generated by pyright.
"""

from .common import PostProcessor

class ExecPP(PostProcessor):
    def __init__(self, downloader, exec_cmd) -> None:
        ...

    def parse_cmd(self, cmd, info):
        ...

    def run(self, info): # -> tuple[list[Unknown], Unknown]:
        ...



class ExecAfterDownloadPP(ExecPP):
    def __init__(self, *args, **kwargs) -> None:
        ...
