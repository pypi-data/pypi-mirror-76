"""Module for LogConsole class."""

from typing import Any
import colorama
from .LogWriter import LogWriter
from .LogItem import LogItem


class LogConsole(LogWriter):
    """Log Writer for writing to console."""

    def __init__(self) -> None:
        """Initialize new LogConsole instance."""
        colorama.init()

    def close(self) -> None:
        """Close LogConsole."""
        pass

    def write(self, *items: Any) -> None:
        """
        Write items to console.

        Args:
            items: Content to write to console.
        """
        for item in items:
            if type(item) is LogItem:
                if item == LogItem.END:
                    print(colorama.Style.RESET_ALL, end='')
                elif item == LogItem.SUCCESS:
                    print(colorama.Style.BRIGHT + colorama.Fore.GREEN, end='')
                elif item == LogItem.INFO:
                    print(colorama.Style.BRIGHT + colorama.Fore.WHITE, end='')
                elif item == LogItem.WARNING:
                    print(colorama.Style.BRIGHT + colorama.Fore.YELLOW, end='')
                elif item == LogItem.ERROR:
                    print(colorama.Style.BRIGHT + colorama.Fore.RED, end='')
                else:
                    raise RuntimeError(f'Unknown item {item}')
            else:
                print(item, end='')
