#!/usr/bin/env python3
"""
    Purpose:
        Test File for init_utils.py
"""

# Python Library Imports
import os
import sys
import pytest
import shutil
from unittest import mock

# Local Library Imports
from magicwand.magicwand_utils import init_utils


###
# Fixtures
###

# go into dir
# init_dir = os.getcwd()


# TODO, use mocks instead of actually creating real dirs.
# https://docs.pytest.org/en/stable/tmpdir.html if necessary
@pytest.fixture(autouse=True)
def clean_up(tmpdir) -> None:
    # remove test folder
    yield
    os.chdir(tmpdir)
    shutil.rmtree("test_folder", ignore_errors=True)


###
# Mocks
###


# N/A


###
# Tests
###


def test_init_folder_exists(tmpdir) -> int:
    """
    Purpose:
        Test to make sure init exits when folder already exists

    """

    # TODO, use mocks instead of actually creating real dirs.
    # https://docs.pytest.org/en/stable/tmpdir.html if necessary
    os.chdir(tmpdir)

    os.mkdir("test_folder")
    init_utils.init("test_folder")
    # check if test_foler is empty

    if os.path.exists("test_folder/mw_data_viewer.py"):
        # TODO, are we still copying python files? We should not be copying
        pytest.fail("File was created in folder that already existed")
        return -1

    return 0


def test_init_folder(tmpdir) -> int:
    """
    Purpose:
        Test to make sure init creates the required files

    """
    os.chdir(tmpdir)
    init_utils.init("test_folder")

    # check if test_foler is empty
    # Check to make sure all files were created
    if os.path.exists("test_folder/mw_data_viewer.py"):
        pytest.fail("File should not be there")
        return -1

    if not os.path.exists("test_folder/data_runs"):
        pytest.fail("Required file not found")
        return -1

    if not os.path.exists("test_folder/configs"):
        pytest.fail("Required file not found")
        return -1

    if not os.path.exists("test_folder/.mw_proj"):
        pytest.fail("Required file not found")
        return -1

    return 0
