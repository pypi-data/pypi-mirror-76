"""Module for the Active-HDL simulator class."""

import os
import shutil
from .SimulatorBase import SimulatorBase
from ..Configuration import Configuration
from ..runner.RunResults import RunCategory
from ..runner.RunResults import RunResults


class ActiveHDL(SimulatorBase):
    """ActiveHDL Simulator class."""

    """Compile parse rules."""
    compile_rules = [
        (r"KERNEL:\s*Warning:", RunCategory.WARNING),
        (r"Error:", RunCategory.ERROR),
        (r"RUNTIME:\s*Fatal Error", RunCategory.ERROR)
    ]

    """Test results parse rules."""
    test_rules = [
        (r"KERNEL:\s*Warning:\s*You are using the Active-HDL Lattice Edition", RunCategory.TEXT),
        (r"KERNEL:\s*Warning:\s*Contact Aldec for available upgrade options", RunCategory.TEXT),
        (r"KERNEL:\s*Warning:", RunCategory.WARNING),
        (r"KERNEL:\s*WARNING:", RunCategory.WARNING),
        (r"EXECUTION::\s*NOTE", RunCategory.INFO),
        (r"EXECUTION::\s*WARNING", RunCategory.WARNING),
        (r"EXECUTION::\s*ERROR", RunCategory.ERROR),
        (r"EXECUTION::\s*FAILURE", RunCategory.ERROR),
        (r"KERNEL:\s*ERROR", RunCategory.ERROR),
        (r"RUNTIME:\s*Fatal Error:", RunCategory.ERROR),
        (r"VSIM:\s*Error:", RunCategory.ERROR)
    ]

    def __init__(self) -> None:
        """Initialize a new ActiveHDL instance."""
        super().__init__('ActiveHDL')

    @classmethod
    def find_path(cls) -> str:
        """Find the path to Active-HDL binaries."""
        # First check environment variable
        path = os.getenv('VHDLTEST_ACTIVEHDL_PATH')
        if path:
            return path

        # Find vsimsa executable
        path = shutil.which('vsimsa')
        if not path:
            return ''

        # Return directory name
        return os.path.dirname(path)

    @classmethod
    def create(cls) -> SimulatorBase:
        """Create an instance of the Active-HDL simulator."""
        return ActiveHDL()

    def compile(self, config: Configuration) -> RunResults:
        """
        Compile VHDL source using Active-HDL compiler.

        Args:
            config (Configuration): Configuration data for compile.
        """
        # Create the directory
        if not os.path.isdir('VHDLTest.out/ActiveHDL'):
            os.makedirs('VHDLTest.out/ActiveHDL')

        # Write the compile script
        with open('VHDLTest.out/ActiveHDL/compile.do', 'w') as stream:
            stream.write('onerror {exit -code 1}\n')
            stream.write('alib work VHDLTest.out/ActiveHDL\n')
            stream.write('set worklib work\n')
            for file in config.files:
                stream.write(f'acom -2008 -dbg {file}\n')

        # Run the compile
        return RunResults.run([
            f'{self._path}/vsimsa',
            '-do',
            'VHDLTest.out/ActiveHDL/compile.do'],
            ActiveHDL.compile_rules)

    def test(self, config: Configuration, test: str) -> RunResults:
        """
        Execute a test-bench using Active-HDL simulator.

        Args:
            config (Configuration): Configuration data for test.
            test (str): Name of test-bench.
        """
        # Write the test script
        with open('VHDLTest.out/ActiveHDL/test.do', 'w') as stream:
            stream.write('onerror {exit -code 1}\n')
            stream.write('set worklib work\n')
            stream.write(f'asim {test}\n')
            stream.write('run -all\n')
            stream.write('endsim\n')
            stream.write('exit -code 0\n')

        # Run the test
        return RunResults.run([
            f'{self._path}/vsimsa',
            '-do',
            'VHDLTest.out/ActiveHDL/test.do'],
            ActiveHDL.test_rules)
