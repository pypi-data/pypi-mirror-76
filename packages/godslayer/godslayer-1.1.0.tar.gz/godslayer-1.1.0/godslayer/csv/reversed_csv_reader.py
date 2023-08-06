"""
This module implements Reversed CSV Reader.
The reversed file reader already exists in PyPI,
however, it doesn't support shift_jis_2004.
@see https://pypi.org/project/file-read-backwards/
"""
import os
from dataclasses import dataclass


@dataclass
class ScanState:
    part: str = ""
    quoting: bool = False


class ReversedCsvReader:
    """This class implements Reversed CSV Reader."""

    @classmethod
    def reversed_lines(cls, file):
        """Generate the lines of file in reverse order."""
        scan_state = ScanState()
        for block in cls.reversed_blocks(file):
            for character in reversed(block):
                yield from cls._reversed_lines(scan_state, character)
        if scan_state.part:
            yield scan_state.part[::-1]

    @staticmethod
    def _reversed_lines(scan_state, character):
        if character == '"':
            scan_state.quoting = not scan_state.quoting
        elif character == "\n" and scan_state.part and not scan_state.quoting:
            yield scan_state.part[::-1]
            scan_state.part = ""
        scan_state.part += character

    @staticmethod
    def reversed_blocks(file, blocksize=4096):
        """Generate blocks of file's contents in reverse order."""
        file.seek(0, os.SEEK_END)
        here = file.tell()
        while here > 0:
            delta = min(blocksize, here)
            here -= delta
            file.seek(here, os.SEEK_SET)
            yield file.read(delta)
