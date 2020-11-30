#!/usr/bin/env python3
"""
    Purpose:
        Test File for mw_runner.py
"""

# Python Library Imports
import os
import json
import sys
import logging
import shutil
import pytest
from unittest import mock

# Local Library Imports
from magicwand.magicwand_utils import init_utils
from magicwand.magicwand_components.mw_runner import MwRunner
from magicwand.magicwand_utils.magicwand_utils import load_json


@pytest.fixture(autouse=True)
def clean_up(tmpdir) -> None:
    # remove test folder
    yield
    os.chdir(tmpdir)
    shutil.rmtree("test_folder", ignore_errors=True)


def test_mw_runner_init() -> int:
    """
    Purpose:
        Do a test run using passed in config
    Args:
        attack (String): Name of attack
        run_config (String): Run configuartion
    Returns:
        (Int): 0 if file passed run, -1 if not
    """
    # Create new runner class
    log_level = logging.INFO

    try:
        mw_runner = MwRunner(log_level)
    except Exception as error:
        logging.error(error)
        pytest.fail("Init fail")

    return 0


def test_mw_runner_pre_run_check(tmpdir) -> int:
    """
    Purpose:
        Do a pre run check with the mw_locust-apachekill.json
    Args:
        tmpdir: Location of tempdir made by pytest
    Returns:
        (Int): 0 if file passed run, -1 if not
    """
    # Create new runner class
    log_level = logging.INFO

    try:
        os.chdir(tmpdir)
        init_utils.init("test_folder")
        os.chdir("test_folder")
        mw_runner = MwRunner(log_level)
        config = mw_runner.pre_run_check(
            "configs/mw_locust-apachekill.json", "test_run"
        )

        # test if data_version already exists
        config2 = mw_runner.pre_run_check(
            "configs/mw_locust-apachekill.json", "test_run"
        )

    except Exception as error:
        logging.error(error)
        pytest.fail("Pre Run check failed")
        return -1

    return 0


def test_mw_runner_pre_run_check_fail(tmpdir) -> int:
    """
    Purpose:
        Do a pre run check with the mw_locust-apachekill.json
    Args:
        tmpdir: Location of tempdir made by pytest
    Returns:
        (Int): 0 if file passed run, -1 if not
    """
    # Create new runner class
    log_level = logging.INFO

    try:
        os.chdir(tmpdir)
        init_utils.init("test_folder")
        os.chdir("test_folder")
        mw_runner = MwRunner(log_level)

        try:
            config = mw_runner.pre_run_check(None, "test_run")
        except TypeError as type_error:
            print(type_error)
        except Exception as error:
            pytest.fail("None check failed?")
            return -1

    except Exception as error:
        logging.error(error)
        pytest.fail("Pre Run check failed")
        return -1

    return 0


def test_mw_runner_build_docker_compose(tmpdir) -> int:
    """
    Purpose:
        Do a build_docker_compose with the mw_locust-apachekill.json
    Args:
        tmpdir: Location of tempdir made by pytest
    Returns:
        (Int): 0 if file passed run, -1 if not
    """
    # Create new runner class
    log_level = logging.INFO

    try:
        os.chdir(tmpdir)
        init_utils.init("test_folder")
        os.chdir("test_folder")
        mw_runner = MwRunner(log_level)
        config = mw_runner.pre_run_check(
            "configs/mw_locust-apachekill.json", "test_run"
        )
        run_json, compoents = mw_runner.build_docker_compose(config, log_level)

    except Exception as error:
        logging.error(error)
        pytest.fail("Build docker compose check failed")
        return -1

    return 0


def make_30_second_test() -> None:
    """
    Purpose:
        Make run 30 seconds
    Args:
        N/A
    Returns:
        N/A
    """
    # sut config path
    config_file = "magicwand_components/suts/mw_apache_wp.json"

    # load sut config
    sut_config = load_json(config_file)

    # set to 30 seconds
    sut_config["run_duration"] = 30

    # save sut config
    try:
        with open(config_file, "w") as outfile:
            json.dump(sut_config, outfile)
    except Exception as error:
        raise OSError(error)


@pytest.mark.slow
@pytest.mark.integration
def test_mw_runner_start_stop_docker_containers(tmpdir) -> int:
    """
    Purpose:
        Do a run with with the mw_locust-apachekill.json
    Args:
        tmpdir: Location of tempdir made by pytest
    Returns:
        (Int): 0 if file passed run, -1 if not
    """
    # Create new runner class
    log_level = logging.INFO

    try:
        # int magicwand folder
        os.chdir(tmpdir)
        init_utils.init("test_folder")
        os.chdir("test_folder")
        data_version = "test_run"
        config_file = "configs/mw_locust-apachekill.json"

        make_30_second_test()

        # start magicwand run
        mw_runner = MwRunner(log_level)
        config = mw_runner.pre_run_check(config_file, data_version)
        run_json, compoents = mw_runner.build_docker_compose(config, log_level)
        counter = 1
        mw_runner.start_docker_containers(run_json, config, counter)
        mw_runner.stop_docker_containers(run_json, counter, data_version)

    except Exception as error:
        logging.error(error)
        pytest.fail("Docker run check failed")
        return -1

    return 0
