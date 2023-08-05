[![CI/Test](https://github.com/Malcolmnixon/VhdlTest/workflows/CI/Test/badge.svg)](https://github.com/Malcolmnixon/VhdlTest/actions?query=workflow%3ACI%2FTest) [![CI/Run](https://github.com/Malcolmnixon/VhdlTest/workflows/CI/Run/badge.svg)](https://github.com/Malcolmnixon/VhdlTest/actions?query=workflow%3ACI%2FRun) [![Documentation Status](https://readthedocs.org/projects/vhdltest/badge/?version=latest)](https://vhdltest.readthedocs.io/en/latest/?badge=latest)

# VHDL Testbench Runner
This python module runs VHDL testbenches and generates a report of the results.
The project [website](https://vhdltest.readthedocs.io/en/latest/) contains more detailed information.
![Console](/docs/source/images/console.png)

## Supported Simulators
It requires a VHDL Simulator be installed on the system. Supported simulators are:
- [GHDL](http://ghdl.free.fr/)
- [Aldec Active-HDL](https://www.aldec.com/en/products/fpga_simulation/active-hdl)

## Installation
VHDL Testbench Runner can be installed by running:
```
python -m pip install VHDLTest
```

## Running
VHDL Testbench Runner can be run by;
```
python -m VHDLTest -c config.yaml
```

## Configuring
VHDL Testbench Runner requires a yaml configuration file to specify the project.
The yaml file lists the VHDL source files and the testbenches to execute.
```
files:
 - module.vhd
 - module_tb.vhd
 
tests:
 - module_tb
```
