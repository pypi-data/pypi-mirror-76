"""Top-level package for God Slayer."""
from typing import List

from godslayer.exceptions import *  # noqa
from godslayer.god_slayer_factory import *  # noqa
from godslayer.last_line_detector import *  # noqa
from godslayer.line_counter import *  # noqa
from godslayer.list_string_matcher import *  # noqa
from godslayer.reader_operator_factory import *  # noqa

__author__ = """Yukihiko Shinoda"""
__email__ = "yuk.hik.future@gmail.com"
__version__ = "1.1.0"

__all__: List[str] = []
# pylint: disable=undefined-variable
__all__ += exceptions.__all__  # type: ignore # noqa
__all__ += god_slayer_factory.__all__  # type: ignore # noqa
__all__ += last_line_detector.__all__  # type: ignore # noqa
__all__ += line_counter.__all__  # type: ignore # noqa
__all__ += list_string_matcher.__all__  # type: ignore # noqa
__all__ += reader_operator_factory.__all__  # type: ignore # noqa
