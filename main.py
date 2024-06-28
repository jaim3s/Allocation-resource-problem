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
    adhoc_network = AdHocNetwork(
        width = 100.0,
        height = 100.0,
        width_span = 10.0,
        height_span = 10.0,
        num_agents = num_agents,
        connection_probability = connection_probability,
        mobility_model = "brownian_motion",
        seed_id = 4070114561247836348
    )
    adhoc_network.run()
    adhoc_network.show_network()
    
if __name__ == "__main__": 
    main()