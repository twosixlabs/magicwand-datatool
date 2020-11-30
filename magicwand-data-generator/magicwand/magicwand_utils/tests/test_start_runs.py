#!/usr/bin/env python3
"""
    Purpose:
        Test File for start_runs.py
"""

# Python Library Imports
import os
import sys
import pytest
import logging
from unittest import mock
import shutil
import glob
import pandas as pd
import json

# Local Library Imports
from magicwand.magicwand_utils import init_utils, start_runs
from magicwand.magicwand_utils.magicwand_utils import load_json


###
# Fixtures
###
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
# Base Functionality Tests
###


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


def is_valid_file(file_path: str, attack: str) -> bool:
    """
    Purpose:
        Test to if file exists in output
    Args:
        file_path (String): location of file
        attack (String): Name of attack
    Returns:
        (Boolean): True if file passed check, False if not
    """
    valid_files = [
        "verify_run.json",
        "tcpdump_verify.csv",
        "rtt_stats.csv",
        "mem_stats.csv",
        "ip_map_sut.csv",
        "ip_map_client.csv",
        "ip_map_attack.csv",
        "ip_map_rtt.csv",
        "tcpdump.pcap",
        "ip_attr_map.csv",
        "apache_stats.csv",
        "run_config.json",
        "cic_flow_labeled.csv",
        "tcpdump.pcap_Flow.csv",
        "run_parms.json",
    ]

    file_name = file_path.split("/")[-1].strip()

    # special check for locust since we dont know exact file name
    if "locust_" in file_name:
        return True

    if file_name in valid_files:

        if "run_parms.json" in file_path:
            with open(file_path) as json_file:
                data = json.load(json_file)
                if "attack" in data:
                    if data["attack"] == attack:
                        return True
                    else:
                        print("Attack " + attack + " does not match " + data["attack"])
                        return False
                elif "benign" in data:
                    if data["benign"] == "mw_locust":
                        return True
                    else:
                        print("Invalid Client")
                        return False

        elif "ip_map_attack.csv" in file_path and attack != "no_attack":
            return True

        return True

        # Just in case we want to check these files more deeply at some point
        # elif "apache_stats.csv" in file_path:
        #     return True

        # elif "ip_map_rtt.csv" in file_path:
        #     return True

        # elif "ip_map_client.csv" in file_path:
        #     return True

        # elif "ip_map_sut.csv" in file_path:
        #     return True

        # elif "mem_stats.csv" in file_path:
        #     return True

        # elif "rtt_stats.csv" in file_path:
        #     return True

        # elif "ip_attr_map.csv" in file_path:
        #     return True

        # elif "tcpdump.pcap" in file_path:
        #     return True

    return False


def magicwand_run(tmpdir, attack: str, run_config: str) -> int:
    """
    Purpose:
        Do a test run using passed in config
    Args:
        tmpdir: the test tmpdir
        attack (String): Name of attack
        run_config (String): Run configuartion
    Returns:
        (Int): 0 if file passed run, -1 if not
    """

    # Create new runner class
    log_level = logging.INFO

    try:
        # int magicwand folder
        os.chdir(tmpdir)
        logging.info(f"Using {tmpdir}")
        init_utils.init("test_folder")
        os.chdir("test_folder")
        data_version = "test_run"
        num_runs = 1

        make_30_second_test()

        status = start_runs.run(run_config, num_runs, data_version, log_level)

        if status != 0:
            pytest.fail("Start Runs Failed")

        # check output folder has required csv and json, and pcap files
        files = glob.glob("data_runs/test_runs/*/*.csv")
        files_json = glob.glob("data_runs/test_runs/*/*.json")
        files_pcap = glob.glob("data_runs/test_runs/*/*.pcap")
        files.extend(files_json)
        files.extend(files_pcap)

        for file_path in files:
            if not is_valid_file(file_path, attack):
                pytest.fail(file_path + " is not valid file")
                return -1

        return 0

    except Exception as error:
        logging.error(error)
        pytest.fail("Docker run check failed")
        return -1


# ###
# # Integration Tests
# ###


@pytest.mark.slow
@pytest.mark.integration
def test_run_ak_default(tmpdir) -> int:
    """
    Purpose:
        Test to make sure apachekill run works
    Args:
        N/A
    Returns:
        (Int): 0 if passed run, -1 if not
    """
    attack = "apachekill"
    run_config = "configs/mw_locust-apachekill.json"
    return magicwand_run(tmpdir, attack, run_config)


@pytest.mark.slow
@pytest.mark.integration
def test_run_sockstress_default(tmpdir) -> int:
    """
    Purpose:
        Test to make sure sockstress run works
    Args:
        N/A
    Returns:
        (Int): 0 if passed run, -1 if not
    """
    attack = "sockstress"
    run_config = "configs/mw_locust-sockstress.json"
    return magicwand_run(tmpdir, attack, run_config)


@pytest.mark.slow
@pytest.mark.integration
def test_run_goloris_default(tmpdir) -> int:
    """
    Purpose:
        Test to make sure goloris run works
    Args:
        N/A
    Returns:
        (Int): 0 if passed run, -1 if not
    """
    attack = "goloris"
    run_config = "configs/mw_locust-goloris.json"
    return magicwand_run(tmpdir, attack, run_config)


@pytest.mark.slow
@pytest.mark.integration
def test_run_sht_rudeadyet_default(tmpdir) -> int:
    """
    Purpose:
        Test to make sure sht-rudeadyet run works
    Args:
        N/A
    Returns:
        (Int): 0 if passed run, -1 if not
    """
    attack = "sht_rudeadyet"
    run_config = "configs/mw_locust-sht_rudeadyet.json"
    return magicwand_run(tmpdir, attack, run_config)


@pytest.mark.slow
@pytest.mark.integration
def test_run_sht_slowread_default(tmpdir) -> int:
    """
    Purpose:
        Test to make sure sht-slowread run works
    Args:
        N/A
    Returns:
        (Int): 0 if passed run, -1 if not
    """
    attack = "sht_slowread"
    run_config = "configs/mw_locust-sht_slowread.json"
    return magicwand_run(tmpdir, attack, run_config)


@pytest.mark.slow
@pytest.mark.integration
def test_run_sht_slowloris_default(tmpdir) -> int:
    """
    Purpose:
        Test to make sure sht-slowloris run works
    Args:
        N/A
    Returns:
        (Int): 0 if passed run, -1 if not
    """
    attack = "sht_slowloris"
    run_config = "configs/mw_locust-sht_slowloris.json"
    return magicwand_run(tmpdir, attack, run_config)


@pytest.mark.slow
@pytest.mark.integration
def test_run_no_attack_default(tmpdir) -> int:
    """
    Purpose:
        Test to make sure no attack run works
    Args:
        N/A
    Returns:
        (Int): 0 if passed run, -1 if not
    """
    attack = "no_attack"
    run_config = "configs/mw_locust-only.json"
    return magicwand_run(tmpdir, attack, run_config)


@pytest.mark.slow
@pytest.mark.integration
def test_run_httpflood_default(tmpdir):
    """
    Purpose:
        Test to make sure no attack run works
    Args:
        N/A
    Returns:
        (Int): 0 if passed run, -1 if not
    """
    attack = "httpflood"
    run_config = "configs/mw_locust-httpflood.json"
    return magicwand_run(attack, run_config)


@pytest.mark.slow
@pytest.mark.integration
def test_run_synflood_default(tmpdir) -> int:
    """
    Purpose:
        Test to make sure no attack run works
    Args:
        N/A
    Returns:
        (Int): 0 if passed run, -1 if not
    """
    attack = "synflood"
    run_config = "configs/mw_locust-synflood.json"
    return magicwand_run(tmpdir, attack, run_config)
