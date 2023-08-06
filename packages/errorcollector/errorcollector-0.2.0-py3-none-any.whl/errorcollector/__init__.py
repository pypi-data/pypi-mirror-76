"""Collects raised error during with statement."""
from typing import List

from errorcollector.error_collector import *  # noqa

__version__ = "0.2.0"

__all__: List[str] = []
# pylint: disable=undefined-variable
__all__ += error_collector.__all__  # type: ignore # noqa
