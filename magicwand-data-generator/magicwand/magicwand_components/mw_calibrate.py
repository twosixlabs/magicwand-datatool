"""
Purpose:
    This file contains the logic for magicwand calibrate.

Copyright:
    This research was developed with funding from the Defense Advanced Research Projects
    Agency (DARPA) under Contract #HR0011-16-C-0060. This document was cleared for
    release under Distribution Statement” A” (Approved for Public Release, Distribution
    Unlimited). The views, opinions, and/or findings expressed are those of the authors
    and should not be interpreted as representing the official views or policies of the
    Department of Defense of the U.S. Government.

    The Government has unlimited rights to use, modify, reproduce, release,
    perform, display, or disclose computer software or computer software
    documentation marked with this legend. Any reproduction of technical data,
    computer software, or portions thereof marked with this legend must also
    reproduce this marking.

    MIT License

    (C) 2020 Two Six Labs, LLC.  All rights reserved.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""


# Lib Updates
import os
import json
import logging
import sys

from magicwand.magicwand_components import *
from magicwand.magicwand_utils.magicwand_utils import load_json, save_json
from magicwand.magicwand_components.attacks import *


# If after 5 attempts, we cant calibrate the attack, we just give up since
# calibration is fuzzy to begin with and has no formal methodology to ensure a
# calibrated system
MAX_RETRIES = 5


def make_150_second_run() -> None:
    """
    Purpose:
        Make run 150 seconds
    Args:
        N/A
    Returns:
        N/A
    """
    # sut config path
    config_file = "magicwand_components/suts/mw_apache_wp.json"

    # load sut config
    sut_config = load_json(config_file)

    # set to 150 seconds
    sut_config["run_duration"] = 150

    save_json(config_file, sut_config)


def generate_data(
    mw_config: str,
    data_version: str,
    log_level: int,
    attack: str,
    calibrate_component: MwComponent,
) -> Dict[str, Any]:
    """
    Purpose:
        Do a calibrate run
    Args:
        mw_config: Run config json
        data_version: Current folder for run
        log_level: Current log level
        attack: which attack to calibrate
        calibrate_component: which componet to use
    Returns:
        metric_data: Dictionary with all post run data
    """

    mw_runner = MwRunner(log_level)
    config = mw_runner.pre_run_check(mw_config, data_version)
    run_json, components = mw_runner.build_docker_compose(config, log_level)
    counter = 1

    if run_json is not None and components is not None:
        mw_runner.start_docker_containers(run_json, config, counter)
        mw_runner.stop_docker_containers(run_json, counter, data_version)
    else:
        raise OSError(f"Problem starting calibrate...")

    # save the metrics we care about
    metric_data = mw_runner.post_run_calibrate(
        run_json, data_version, attack, calibrate_component
    )

    return metric_data


def update_configs(
    run_json_attack: Dict[str, Any],
    run_json_benign: Dict[str, Any],
    attack_config: str,
    benign_config: str,
    attack: str,
) -> None:
    """
    Purpose:
        Update configs based on the calibration. Could include increasing/decreasing threads/connections per thread depending on the user's resources.
    Args:
        run_json_attack: the updated attack config
        run_json_benign: the updated benign config
        attack_config: the run attack config file path
        benign_config: the run benign config file path
        attack: current attack,
    Returns:
        N/A
    """

    if attack == "apachekill":

        # update benign num_ips?
        benign_json = load_json(benign_config)
        benign_json["client_options"]["num_ips"] = run_json_benign["benign"][
            "client_options"
        ]["num_ips"]
        save_json(benign_config, benign_json)

        # update attack config
        attack_json = load_json(attack_config)
        attack_json["attack_options"]["ak_num_threads"] = run_json_attack["attack"][
            "attack_options"
        ]["ak_num_threads"]
        save_json(attack_config, attack_json)

        # Update sut config
        config_file = "magicwand_components/suts/mw_apache_wp.json"
        sut_config = load_json(config_file)
        sut_config["max_clients"] = run_json_attack["sut"]["max_clients"]
        sut_config["run_duration"] = run_json_attack["sut"]["run_duration"]
        save_json(config_file, sut_config)
    else:
        raise TypeError(f"Invalid attack {attack}")


def calibrate(attack: str, log_level: int) -> int:
    """
    Purpose:
        Setup calibrate
    Args:
        attack: which attack to calibrate
        log_level: Current log level
    Returns:
        status: 0 if passed, -1 if failed
    """
    # TODO can massge this whenever we add new attacks
    valid_attacks = ["apachekill"]

    if attack == "apachekill":
        attack_config = "configs/apachekill-only.json"
        calibrate_component = Apachekill(log_level)
        attack_component_config = "magicwand_components/attacks/apachekill.json"
    else:
        raise ValueError(f"Invalid attack {attack}, must be from {valid_attacks}")

    benign_config = "configs/mw_locust-only.json"
    benign_component_config = "magicwand_components/benign/mw_locust.json"

    data_version = "mw_calibrate_runs"

    # change run time to 150
    make_150_second_run()

    calibrate_count = 0
    status = 0

    while calibrate_count < MAX_RETRIES:
        # Do a benign run as a control run for comparing results
        benign_data = generate_data(
            benign_config, data_version, log_level, attack, calibrate_component
        )

        # Do an attack run with the current config settings to see if the attack affects the SUT
        attack_data = generate_data(
            attack_config, data_version, log_level, attack, calibrate_component
        )

        # Load the results from the runs
        run_json_attack = load_json(attack_data["run_json_loc"])
        run_json_benign = load_json(benign_data["run_json_loc"])

        apache_df = benign_data["apache_df"]
        apache_df_attack = attack_data["apache_df"]

        rtt_df = benign_data["rtt_df"]
        rtt_df_attack = attack_data["rtt_df"]

        mem_df = benign_data["mem_df"]
        mem_df_attack = attack_data["mem_df"]

        # Compare the results of benign vs attack to ensure attack affected the SUT
        (
            passed_checks,
            new_run_json_attack,
            new_run_json_benign,
        ) = calibrate_component.ratio_checker(
            run_json_attack,
            run_json_benign,
            apache_df,
            apache_df_attack,
            rtt_df,
            rtt_df_attack,
            mem_df,
            mem_df_attack,
        )

        # update the configs
        update_configs(
            new_run_json_attack,
            new_run_json_benign,
            attack_component_config,
            benign_component_config,
            attack,
        )

        # If the calibration checks all passed, then the attack is calibrated.
        # Once attack is calibrated, we can exit the loop and return success
        # If it fails then go through the calibration process again
        if passed_checks:
            status = 0
            break
        else:
            calibrate_count += 1

        if calibrate_count > MAX_RETRIES:
            logging.info("Giving up after 5 failed runs...")
            status = -1
            break

    return status
