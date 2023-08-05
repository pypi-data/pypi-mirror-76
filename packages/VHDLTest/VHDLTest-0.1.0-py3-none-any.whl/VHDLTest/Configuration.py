"""Module for VHDLTest Configuration class."""

from typing import List, Dict, Any
import os
import yaml


class Configuration(object):
    """YAML configuration class."""

    _doc: Dict[str, Any]

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

        # Save the dictionary
        self._doc = doc

    @property
    def doc(self) -> Dict[str, Any]:
        """Get the YAML document."""
        return self._doc or {}

    @property
    def files(self) -> List[str]:
        """Get the files mentioned in the configuration."""
        file_list = self.doc.get('files')
        return file_list if isinstance(file_list, list) else []

    @property
    def tests(self) -> List[str]:
        """Get the tests mentioned in the configuration."""
        test_list = self.doc.get('tests')
        return test_list if isinstance(test_list, list) else []
