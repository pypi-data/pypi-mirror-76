"""Module for RunResults class and support types."""

import subprocess
import re
from datetime import datetime
from enum import Enum
from typing import TypeVar, List, Tuple
from ..logger.Log import Log


class RunCategory(Enum):
    """Enumeration of RunResults categories."""

    TEXT = 0
    INFO = 1
    WARNING = 2
    ERROR = 3

    @property
    def is_info(self) -> bool:
        """Test if category is INFO or higher."""
        return self.value >= RunCategory.INFO.value

    @property
    def is_warning(self) -> bool:
        """Test if category is WARNING or higher."""
        return self.value >= RunCategory.WARNING.value

    @property
    def is_error(self) -> bool:
        """Test if category is ERROR."""
        return self.value >= RunCategory.WARNING.value


class RunLine(object):
    """Class for RunResults line."""

    def __init__(self,
                 text: str,
                 category: RunCategory) -> None:
        """
        Initialize a new RunLine instance.

        Args:
            text (str): Text of the line.
            category (RunCategory): Category of the line.
        """
        self.text = text
        self.category = category


T = TypeVar('T', bound='RunResults')


class RunResults(object):
    """RunResults class."""

    def __init__(self,
                 start: datetime,
                 duration: float,
                 returncode: int,
                 output: str,
                 rules: List[Tuple[str, RunCategory]]) -> None:
        """
        Initialize a new RunResults instance.

        Args:
            start (datetime): Run start timestamp.
            duration (float): Run duration in seconds.
            returncode (int): Run application return code.
            output (str): Run application output string.
            rules: Run parse rules to classify output lines.
        """
        self.start = start
        self.duration = duration
        self.returncode = returncode
        self.output = output
        self.lines = []

        # Process all lines appending output
        for line in output.splitlines():
            # Look for matching rule
            category = RunCategory.TEXT
            for rule in rules:
                if re.match(rule[0], line):
                    category = rule[1]
                    break

            # Append the line
            self.lines.append(RunLine(line, category))

    @property
    def category(self) -> RunCategory:
        """Get the RunCategory associated with the entire run."""
        # Check for non-zero returncode
        if self.returncode != 0:
            return RunCategory.ERROR

        # If no lines then just return text
        if not self.lines:
            return RunCategory.TEXT

        # Return the maximum value
        return RunCategory(max([line.category.value for line in self.lines]))

    @property
    def info(self) -> bool:
        """Test if the runs category is INFO or higher."""
        return self.category.value >= RunCategory.INFO.value

    @property
    def warning(self) -> bool:
        """Test if the runs category is WARNING or higher."""
        return self.category.value >= RunCategory.WARNING.value

    @property
    def error(self) -> bool:
        """Test if the runs category is ERROR or higher."""
        return self.category.value >= RunCategory.ERROR.value

    @property
    def failure(self) -> bool:
        """Test if the run failed."""
        return self.returncode != 0

    @property
    def error_info(self) -> str:
        """Get text describing the run error."""
        # Get the error lines
        errors = [line.text for line in self.lines if line.category.is_error]

        # Add any returncode info
        if self.returncode != 0:
            errors.append(f'Program terminated with returncode {self.returncode}')

        # Join into single line
        return '\n'.join(errors)

    def print(self,
              log: Log,
              level: RunCategory = RunCategory.TEXT) -> None:
        """
        Print RunResults to log.

        Args:
            log (Log): Log to write run to.
            level (RunCategory): Level of items to include.
        """
        for line in self.lines:
            # Skip lines below the level threshold
            if line.category.value < level.value:
                continue

            # Log the lines with suitable coloring
            if line.category == RunCategory.INFO:
                log.write(Log.info, line.text, Log.end, '\n')
            elif line.category == RunCategory.WARNING:
                log.write(Log.warning, line.text, Log.end, '\n')
            elif line.category == RunCategory.ERROR:
                log.write(Log.error, line.text, Log.end, '\n')
            else:
                log.write(line.text, '\n')

    @staticmethod
    def run(args: List[str],
            rules: List[Tuple[str, RunCategory]]) -> T:
        """
        Run program and return new RunResults.

        Args:
            args (List[str]): List of program arguments.
            rules: Parse rules to categorize output lines.
        """
        # Capture the start time
        start = datetime.now()

        # Create results
        try:
            # Run the process and capture the output
            out = subprocess.check_output(args, stderr=subprocess.STDOUT)
            returncode = 0
        except subprocess.CalledProcessError as err:
            out = err.output
            returncode = err.returncode

        # Calculate the duration
        end = datetime.now()
        duration = (end - start).total_seconds()

        # Return the results
        return RunResults(
            start,
            duration,
            returncode,
            out.decode('utf-8'),
            rules)
