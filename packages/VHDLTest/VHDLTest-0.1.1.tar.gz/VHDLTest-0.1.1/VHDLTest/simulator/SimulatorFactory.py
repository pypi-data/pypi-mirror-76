"""Module for SimulatorFactory class."""

from typing import List, Type, Optional
from .SimulatorBase import SimulatorBase
from .ActiveHDL import ActiveHDL
from .GHDL import GHDL


class SimulatorFactory(object):
    """Factory for VHDL simulators."""

    @staticmethod
    def simulator_list() -> List[Type[SimulatorBase]]:
        """Get the list of supported simulators."""
        return [
            ActiveHDL,
            GHDL
        ]

    @staticmethod
    def available_simulators() -> List[Type[SimulatorBase]]:
        """Get the list of available simulators."""
        return [sim for sim in SimulatorFactory.simulator_list() if sim.is_available()]

    @staticmethod
    def create_simulator() -> Optional[SimulatorBase]:
        """Create a simulator."""
        # Get the list of available simulators and return None if none available
        available = SimulatorFactory.available_simulators()
        if not available:
            return None

        # Create an instance of the first available simulator
        return available[0].create()
