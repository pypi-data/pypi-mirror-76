"""Module for VHDLTest Configuration class."""

from typing import List
import os
import yaml


class Configuration(object):
    """YAML configuration class."""

    files: List[str]
    tests: List[str]

    def __init__(self, filename: str) -> None:
        """
        Initialize a new Configuration instance.

        Args:
            filename (str): YAML configuration file name.
        """
        # Fail if file doesn't exist
        if not os.path.isfile(filename):
            raise RuntimeError(f'Configuration file {filename} not found.')

        # Load the configuration file contents
        with open(filename, 'r') as stream:
            contents = stream.read()

        # Parse the configuration file contents
        doc = yaml.load(contents, Loader=yaml.SafeLoader)
        if not isinstance(doc, dict):
            raise RuntimeError(f'Malformed configuration file {filename}')

        # Get the list of files
        files = doc.get('files')
        self.files = files if isinstance(files, list) else []

        # Get the list of tests
        tests = doc.get('tests')
        self.tests = tests if isinstance(files, list) else []
