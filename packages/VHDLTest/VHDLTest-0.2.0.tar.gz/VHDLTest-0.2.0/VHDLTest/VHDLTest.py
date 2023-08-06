"""Module for VHDLTest application class."""

import argparse
import sys
from typing import Optional, Dict
from junit_xml import TestSuite, TestCase
from datetime import datetime
from .simulator.SimulatorBase import SimulatorBase
from .simulator.SimulatorFactory import SimulatorFactory
from .Configuration import Configuration
from .logger.Log import Log
from .runner.RunResults import RunCategory
from .runner.RunResults import RunResults


class VHDLTest(object):
    """VHDLTest application class."""

    _log: Optional[Log]
    _config: Optional[Configuration]
    _simulator: Optional[SimulatorBase]
    _compile_result: Optional[RunResults]
    _test_result: Dict[str, RunResults]

    # VHDLTest version
    version = "0.2.0"

    def __init__(self) -> None:
        """Initialize a new VHDLTest instance."""
        self._args = None
        self._log = None
        self._config = None
        self._simulator = None
        self._compile_result = None
        self._test_results = {}
        self._test_count = 0
        self._test_passed = 0
        self._test_failed = 0
        self._total_duration = 0.0
        self._elapsed_duration = 0.0

    def parse_arguments(self) -> None:
        """Parse command-line arguments into _args."""
        # Construct the argument parser
        parser = argparse.ArgumentParser(
            prog='VHDL Test-bench Runner (VHDLTest)',
            description='''Runs VHDL Test-benches and generates a report of the
                         passes and failures. Reference documentation is located
                         at https://github.com/Malcolmnixon/VhdlTest''')
        parser.add_argument('-c', '--config', help='Configuration file')
        parser.add_argument('-l', '--log', help='Write to log file')
        parser.add_argument('-j', '--junit', help='Generate JUnit xml file')
        parser.add_argument('-t', '--tests', nargs='+', help='List of test-benches to run')
        parser.add_argument('-s', '--simulator', default='', help='Specify simulator (E.G. GHDL)')
        parser.add_argument('-v', '--verbose', default=False, action='store_true', help='Verbose logging of output')
        parser.add_argument('--exit-0', default=False, action='store_true', help='Exit with code 0 even if tests fail')
        parser.add_argument('--version', default=False, action='store_true', help='Display version information')

        # If no arguments are provided then print the help information
        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(1)

        # Parse the arguments
        self._args = parser.parse_args()

        # Check for version
        if self._args.version:
            print(f'VHDL Test-bench Runner (VHDLTest) version {VHDLTest.version}')
            sys.exit(0)

        # Ensure we have a configuration
        if self._args.config is None:
            parser.print_help()
            sys.exit(1)

    def compile_source(self) -> None:
        """Compile VHDL source files into library."""
        # Compile the code
        self._log.write(f'Compiling files using {self._simulator.name}...\n')
        self._compile_result = self._simulator.compile(self._config)

        # Print compile log on verbose or compile warning/error
        level = RunCategory.TEXT if self._args.verbose or self._compile_result.warning else RunCategory.INFO
        self._compile_result.print(self._log, level)

        # On compile error write error message
        if self._compile_result.error:
            self._log.write(Log.error,
                            'Error: Compile of source files failed',
                            Log.end,
                            '\n\n')
            sys.exit(1)

        # Report compile success
        self._log.write(Log.success, 'done', Log.end, '\n\n')

    def run_tests(self) -> None:
        """Run VHDL test benches and gather results."""
        # Run the tests
        self._test_results = {}
        self._test_passed = 0
        self._test_failed = 0
        self._total_duration = 0.0
        for test in self._config.tests:
            # Log starting the test
            self._log.write(f'Starting {test}\n')

            # Run the test and save the result
            result = self._simulator.test(self._config, test)
            self._test_results[test] = result
            self._total_duration += result.duration

            # Print test log on verbose or test warning/error
            level = RunCategory.TEXT if self._args.verbose or result.warning else RunCategory.INFO
            result.print(self._log, level)

            # Log the result
            if result.error:
                self._log.write(Log.error, 'fail ', Log.end, f'{test} ({result.duration:.1f} seconds)\n')
                self._test_failed += 1
            else:
                self._log.write(Log.success, 'pass ', Log.end, f'{test} ({result.duration:.1f} seconds)\n')
                self._test_passed += 1

            # Add separator after test
            self._log.write('\n')

    def emit_junit(self) -> None:
        """Emit JUnit report file containing test results."""
        # Print generating message
        self._log.write(f'Generating JUnit output {self._args.junit}\n')

        # Create the test cases
        test_cases = []
        for test in self._config.tests:
            result = self._test_results[test]

            # Create the test case
            test_case = TestCase(test, classname=test, elapsed_sec=result.duration, stdout=result.output)

            # Detect failures or errors
            if result.failure:
                # Test failed, could not get results
                test_case.add_failure_info(output=result.error_info)
            elif result.error:
                # Test detected error
                test_case.add_error_info(message=result.error_info)

            test_cases.append(test_case)

        # Create the test suite
        test_suite = TestSuite('testsuite', test_cases)

        # Write test suite to file
        with open(self._args.junit, 'w') as f:
            TestSuite.to_file(f, [test_suite])

        # Report compile success
        self._log.write(Log.success, 'done', Log.end, '\n\n')

    def print_summary(self) -> None:
        """Print test summary information to log."""
        # Print summary list
        self._log.write('==== Summary ========================================\n')
        for test in self._config.tests:
            result = self._test_results[test]
            if result.error:
                self._log.write(Log.error, 'fail ', Log.end, f'{test} ({result.duration:.1f} seconds)\n')
            else:
                self._log.write(Log.success, 'pass ', Log.end, f'{test} ({result.duration:.1f} seconds)\n')

        # Print summary statistics
        self._log.write('=====================================================\n')
        if self._test_count == 0:
            self._log.write(Log.warning, 'No tests were run!', Log.end, '\n')
        if self._test_passed != 0:
            self._log.write(Log.success, 'pass ', Log.end, f'{self._test_passed} of {self._test_count}\n')
        if self._test_failed != 0:
            self._log.write(Log.error, 'fail ', Log.end, f'{self._test_failed} of {self._test_count}\n')

        # Print time information
        self._log.write('=====================================================\n')
        self._log.write(f'Total time was {self._total_duration:.1f} seconds\n')
        self._log.write(f'Elapsed time was {self._elapsed_duration:.1f} seconds\n')
        self._log.write('=====================================================\n')

        # Print final warning if any failed
        if self._test_failed != 0:
            self._log.write(Log.error, 'Some failed!', Log.end, '\n')

    def run(self) -> None:
        """Run all VHDLTest steps."""
        # Parse arguments
        self.parse_arguments()

        # Construct the logger
        self._log = Log()
        if self._args.log is not None:
            self._log.add_log_file(self._args.log)

        # Print the banner and capture the start time
        self._log.write('VHDL Test-bench Runner (VHDLTest)\n\n')
        elapsed_start = datetime.now()

        # Read the configuration
        self._config = Configuration(self._args.config)

        # Override configuration with command line arguments
        if self._args.tests:
            self._config.tests = self._args.tests

        # Count the number of tests
        self._test_count = len(self._config.tests)

        # Create a simulator
        self._simulator = SimulatorFactory.create_simulator(self._args.simulator)
        if self._simulator is None:
            self._log.write(Log.error,
                            'Error: Simulator not found. Please add simulator to the path',
                            Log.end,
                            '\n')
            sys.exit(1)

        # Compile the code
        self.compile_source()

        # Run the tests
        self.run_tests()
        elapsed_end = datetime.now()
        self._elapsed_duration = (elapsed_end - elapsed_start).total_seconds()

        # Generate JUnit output
        if self._args.junit is not None:
            self.emit_junit()

        # Print summary list
        self.print_summary()

        # Generate error code if necessary
        if self._test_failed != 0 and not self._args.exit_0:
            sys.exit(1)
