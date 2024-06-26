#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python program for simulating Ad Hoc networks and the partition tasking problem
"""


from scripts.adhoc_network import AdHocNetwork
from scripts.generator import Generator

def main():
    """
    Run code.
    """

    num_nodes = 10
    connection_probability = 0.3
    adhoc_network = AdHocNetwork(
        width = 100.0,
        height = 100.0,
        width_span = 10.0,
        height_span = 10.0,
        num_nodes = num_nodes,
        connection_probability = connection_probability
    )
    adhoc_network.show_network()

if __name__ == "__main__": 
    main()