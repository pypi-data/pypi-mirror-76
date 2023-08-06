"""Module for SimulatorFactory class."""

from typing import Dict, Type, Optional
from .SimulatorBase import SimulatorBase
from .ActiveHDL import ActiveHDL
from .GHDL import GHDL


class SimulatorFactory(object):
    """Factory for VHDL simulators."""

    """List of simulators."""
    _simulators: Dict[str, Type[SimulatorBase]] = {
        'activehdl': ActiveHDL,
        'ghdl': GHDL
    }

    @staticmethod
    def create_simulator(name: str) -> Optional[SimulatorBase]:
        """Create a simulator."""
        if name:
            # Find simulator in dictionary
            sim_type = SimulatorFactory._simulators.get(name.lower())
        else:
            # Select first available
            sim_type = next((s for s in SimulatorFactory._simulators.values() if s.is_available()), None)

        # Handle not found or not available
        if not sim_type or not sim_type.is_available():
            return None

        # Create an instance of the first available simulator
        return sim_type.create()
