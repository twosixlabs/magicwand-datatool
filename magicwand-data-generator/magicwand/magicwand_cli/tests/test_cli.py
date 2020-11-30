#!/usr/bin/env python3
"""
    Purpose:
        Test File for cli.py
"""

# Python Library Imports
import os
import sys
import pytest
from unittest import mock

# Local Library Imports
from magicwand.magicwand_cli import cli


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


def test_setup_magicwand_cli():
    """
    Purpose:
        Test Setting up the CLI

    """

    cli.setup_magicwand_cli()
