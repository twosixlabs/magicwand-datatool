#!/usr/bin/env python3
"""
    Purpose:
        Test File for magicwand_utils.py
"""

# Python Library Imports
import os
import sys
import pytest
from unittest import mock

# Local Library Imports
from magicwand.magicwand_utils import magicwand_utils

curr_dir = os.getcwd()
###
# Fixtures
###


# N/A


###
# Mocks
###


# N/A


###
# Tests
###


def test_convert_pcap_fail() -> int:
    """
    Purpose:
        Test to fail convert pcap
    Args:
        N/A
    Returns:
        (Int): 0 if passed run
    """
    pcap = "PCAP location"
    output = "cic_flow.csv"
    force = True

    status = magicwand_utils.convert_pcap(pcap, output, force)

    if status == 0:
        pytest.fail("should have failed")

    return 0


def test_convert_pcap() -> int:
    """
    Purpose:
        Test to make sure convert works
    Args:
        N/A
    Returns:
        (Int): 0 if passed run
    """
    pcap = curr_dir + "/test_data/tcpdump.pcap"
    output = "cic_flow.csv"
    force = True

    status = magicwand_utils.convert_pcap(pcap, output, force)

    if status != 0:
        pytest.fail("should have worked")

    # remove test file
    os.remove(curr_dir + "/test_data/cic_flow.csv")

    return 0
