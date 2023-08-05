"""Module for LogFile class."""

from typing import Any
from .LogWriter import LogWriter
from .LogItem import LogItem


class LogFile(LogWriter):
    """Log Writer for writing to files."""

    def __init__(self, filename: str) -> None:
        """
        Initialize new LogFile instance.

        Args:
            filename (str): Log file name.
        """
        self._stream = open(filename, 'w')

    def close(self) -> None:
        """Close log file."""
        self._stream.close()

    def write(self, *items: Any) -> None:
        """
        Write content to log file.

        Args:
            items: Content to write to log file.
        """
        for item in items:
            if type(item) is not LogItem:
                self._stream.write(item)
