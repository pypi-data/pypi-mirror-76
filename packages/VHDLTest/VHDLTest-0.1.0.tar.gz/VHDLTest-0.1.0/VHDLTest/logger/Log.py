"""Module for Log class."""

from typing import Any, List
from .LogWriter import LogWriter
from .LogConsole import LogConsole
from .LogFile import LogFile
from .LogItem import LogItem


class Log(object):
    """Log class to manage logging."""

    _loggers: List[LogWriter]

    # Simple access to LogItem types
    end = LogItem.END
    success = LogItem.SUCCESS
    info = LogItem.INFO
    warning = LogItem.WARNING
    error = LogItem.ERROR

    def __init__(self) -> None:
        """Initialize a new Log instance."""
        # Start with only console logger
        self._loggers = [LogConsole()]

    def add_log_file(self, filename: str) -> None:
        """
        Add a file-logger.

        Args:
            filename (str): Name of the log file.
        """
        # Append new LogFile to loggers
        self._loggers.append(LogFile(filename))

    def close(self) -> None:
        """Close and dispose of all loggers (other than console)."""
        # Close all loggers
        for logger in self._loggers:
            logger.close()

        # Dispose of all extra loggers
        self._loggers = self._loggers[0:1]

    def write(self, *args: Any) -> None:
        """
        Write content to loggers.

        Args:
            args: Content to write to loggers.
        """
        # Send to all loggers
        for logger in self._loggers:
            logger.write(*args)
