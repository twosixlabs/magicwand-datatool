#!/usr/bin/env python3
"""
    Purpose:
        Test File for mw_calibrate.py
"""

# Python Library Imports
import json
import logging
import os
import pytest
import sys
import shutil
from unittest import mock

# Local Library Imports
from magicwand.magicwand_utils import init_utils
from magicwand.magicwand_components.mw_runner import MwRunner
from magicwand.magicwand_utils.magicwand_utils import load_json
import magicwand.magicwand_components.mw_calibrate as mw_calibrate


@pytest.fixture(autouse=True)
def clean_up(tmpdir) -> None:
    # remove test folder
    yield
    os.chdir(tmpdir)
    shutil.rmtree("test_folder", ignore_errors=True)


def make_weak_ak() -> None:
    """
    Purpose:
        Make a weak apachekill
    Args:
        N/A
    Returns:
        N/A
    """
    # ak config path
    config_file = "magicwand_components/attacks/apachekill.json"

    # load ak config
    attack_config = load_json(config_file)

    # make attack weak
    attack_config["ak_num_threads"] = 1

    # save sut config
    try:
        with open(config_file, "w") as outfile:
            json.dump(attack_config, outfile)
    except Exception as error:
        raise OSError(error)


def test_fake_attack() -> int:
    """
    Purpose:
        Test a fake attack on calibrate
    Args:
        N/A
    Returns:
        (Int): 0 if file passed run, -1 if not
    """
    # Create new runner class
    log_level = logging.INFO
    attack = "fake_attack"

    try:
        mw_calibrate.calibrate(attack, log_level)
    except ValueError as type_error:
        logging.info(type_error)
    except Exception as error:
        pytest.fail("Type check failed?")
        return -1

    return 0


@pytest.mark.slow
@pytest.mark.integration
def test_calibrate_apachekill(tmpdir) -> int:
    """
    Purpose:
        Test a appachekill calibration run
    Args:
        tmpdir: Location of tmpdir made by pytest
    Returns:
        (Int): 0 if file passed run, -1 if not
    """
    # Create new runner class
    log_level = logging.INFO
    attack = "apachekill"

    try:
        os.chdir(tmpdir)
        init_utils.init("test_folder")
        os.chdir("test_folder")
        data_version = "test_run"
        mw_calibrate.calibrate(attack, log_level)
    except Exception as error:
        pytest.fail(error)
        return -1

    return 0


@pytest.mark.slow
@pytest.mark.integration
def test_calibrate_apachekill_weak(tmpdir) -> int:
    """
    Purpose:
        Test a appachekill calibration run
    Args:
        tmpdir: Location of tmpdir made by pytest
    Returns:
        (Int): 0 if file passed run, -1 if not
    """
    # Create new runner class
    log_level = logging.INFO
    attack = "apachekill"

    try:
        os.chdir(tmpdir)
        init_utils.init("test_folder")
        os.chdir("test_folder")
        data_version = "test_run"

        # Edit the ak config file
        make_weak_ak()

        mw_calibrate.calibrate(attack, log_level)
    except Exception as error:
        pytest.fail(error)
        return -1

    return 0
