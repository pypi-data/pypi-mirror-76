"""Module for LogItem enumeration."""
from enum import Enum


class LogItem(Enum):
    """Enumeration of the types of log items."""

    END = 0
    SUCCESS = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
