"""
This type stub file was generated by pyright.
"""

from .common import PostProcessor

class XAttrMetadataPP(PostProcessor):
    """Set extended attributes on downloaded file (if xattr support is found)

    More info about extended attributes for media:
        http://freedesktop.org/wiki/CommonExtendedAttributes/
        http://www.freedesktop.org/wiki/PhreedomDraft/
        http://dublincore.org/documents/usageguide/elements.shtml

    TODO:
        * capture youtube keywords and put them in 'user.dublincore.subject' (comma-separated)
        * figure out which xattrs can be used for 'duration', 'thumbnail', 'resolution'
    """
    XATTR_MAPPING = ...
    def run(self, info): # -> tuple[list[Unknown], Unknown]:
        ...
