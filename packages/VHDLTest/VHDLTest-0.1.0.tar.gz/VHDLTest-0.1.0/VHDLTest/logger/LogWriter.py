"""Module for LogWriter interface."""
from typing import Any


class LogWriter(object):
    """Base class for log writers."""

    def close(self) -> None:
        """Close the writer."""
        raise NotImplementedError

    def write(self, *items: Any) -> None:
        """
        Write content to the log.

        Args:
            items: Content to write.
        """
        raise NotImplementedError
