#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python program for simulating Ad Hoc networks and the partition tasking problem
"""

from scripts.program import Program
from scripts.adhoc_network import AdHocNetwork


def main():
    """
    Run code.
    """

    num_agents = 5
    connection_probability = 1.0
    program = Program()
    program.delete_folders()
    parameters = program.read_parameters("parameters1.txt")
    adhoc_network = AdHocNetwork(**parameters)
    adhoc_network.run()
    
if __name__ == "__main__": 
    main()