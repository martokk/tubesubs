"""
This type stub file was generated by pyright.
"""

from ..utils import classproperty

class FileDownloader:
    """File Downloader class.

    File downloader objects are the ones responsible of downloading the
    actual video file and writing it to disk.

    File downloaders accept a lot of parameters. In order not to saturate
    the object constructor with arguments, it receives a dictionary of
    options instead.

    Available options:

    verbose:            Print additional info to stdout.
    quiet:              Do not print messages to stdout.
    ratelimit:          Download speed limit, in bytes/sec.
    continuedl:         Attempt to continue downloads if possible
    throttledratelimit: Assume the download is being throttled below this speed (bytes/sec)
    retries:            Number of times to retry for HTTP error 5xx
    file_access_retries:   Number of times to retry on file access error
    buffersize:         Size of download buffer in bytes.
    noresizebuffer:     Do not automatically resize the download buffer.
    continuedl:         Try to continue downloads if possible.
    noprogress:         Do not print the progress bar.
    nopart:             Do not use temporary .part files.
    updatetime:         Use the Last-modified header to set output file timestamps.
    test:               Download only first bytes to test the downloader.
    min_filesize:       Skip files smaller than this size
    max_filesize:       Skip files larger than this size
    xattr_set_filesize: Set ytdl.filesize user xattribute with expected size.
    external_downloader_args:  A dictionary of downloader keys (in lower case)
                        and a list of additional command-line arguments for the
                        executable. Use 'default' as the name for arguments to be
                        passed to all downloaders. For compatibility with youtube-dl,
                        a single list of args can also be used
    hls_use_mpegts:     Use the mpegts container for HLS videos.
    http_chunk_size:    Size of a chunk for chunk-based HTTP downloading. May be
                        useful for bypassing bandwidth throttling imposed by
                        a webserver (experimental)
    progress_template:  See YoutubeDL.py
    retry_sleep_functions: See YoutubeDL.py

    Subclasses of this one must re-define the real_download method.
    """
    _TEST_FILE_SIZE = ...
    params = ...
    def __init__(self, ydl, params) -> None:
        """Create a FileDownloader object with the given options."""
        ...

    def to_screen(self, *args, **kargs): # -> None:
        ...

    __to_screen = ...
    @classproperty
    def FD_NAME(cls): # -> str:
        ...

    @staticmethod
    def format_seconds(seconds): # -> LiteralString | Literal[' Unknown', '--:--:--']:
        ...

    @classmethod
    def format_eta(cls, seconds): # -> str:
        ...

    @staticmethod
    def calc_percent(byte_counter, data_len): # -> float | None:
        ...

    @staticmethod
    def format_percent(percent): # -> str:
        ...

    @staticmethod
    def calc_eta(start, now, total, current): # -> int | None:
        ...

    @staticmethod
    def calc_speed(start, now, bytes): # -> None:
        ...

    @staticmethod
    def format_speed(speed): # -> str:
        ...

    @staticmethod
    def format_retries(retries): # -> int | Literal['inf']:
        ...

    @staticmethod
    def best_block_size(elapsed_time, bytes): # -> int:
        ...

    @staticmethod
    def parse_bytes(bytestr): # -> None:
        """Parse a string indicating a byte quantity into an integer."""
        ...

    def slow_down(self, start_time, now, byte_counter): # -> None:
        """Sleep if the download speed is over the rate limit."""
        ...

    def temp_name(self, filename):
        """Returns a temporary filename for the given filename."""
        ...

    def undo_temp_name(self, filename):
        ...

    def ytdl_filename(self, filename):
        ...

    def wrap_file_access(action, *, fatal=...): # -> partial[partialmethod[Unknown]]:
        ...

    @wrap_file_access('open', fatal=True)
    def sanitize_open(self, filename, open_mode): # -> tuple[BinaryIO | TextIO | locked_file | Unknown, Unknown | str]:
        ...

    @wrap_file_access('remove')
    def try_remove(self, filename): # -> None:
        ...

    @wrap_file_access('rename')
    def try_rename(self, old_filename, new_filename): # -> None:
        ...

    def try_utime(self, filename, last_modified_hdr): # -> int | None:
        """Try to set the last-modified time of the given file."""
        ...

    def report_destination(self, filename): # -> None:
        """Report destination filename."""
        ...

    ProgressStyles = ...
    def report_progress(self, s): # -> None:
        ...

    def report_resuming_byte(self, resume_len): # -> None:
        """Report attempt to resume at given byte."""
        ...

    def report_retry(self, err, count, retries, frag_index=..., fatal=...): # -> None:
        """Report retry"""
        ...

    def report_unable_to_resume(self): # -> None:
        """Report it was impossible to resume download."""
        ...

    @staticmethod
    def supports_manifest(manifest): # -> None:
        """ Whether the downloader can download the fragments from the manifest.
        Redefine in subclasses if needed. """
        ...

    def download(self, filename, info_dict, subtitle=...): # -> tuple[Literal[True], Literal[False]] | tuple[Unknown, Literal[True]]:
        """Download to a filename using the info from info_dict
        Return True on success and False otherwise
        """
        ...

    def real_download(self, filename, info_dict):
        """Real download process. Redefine in subclasses."""
        ...

    def add_progress_hook(self, ph): # -> None:
        ...
