"""
Purpose:
    This file contains the logic to start magicwand experiments.

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

# Python Library Imports
import datetime
import json
import os
import shutil
import signal
import sys
import time
import logging
from functools import partial
from typing import Any, Dict
import pandas as pd  # type: ignore

# Local Python Library Imports
from magicwand.magicwand_config.config import Config
from magicwand.magicwand_utils.magicwand_utils import get_logger

from magicwand.magicwand_components import *


def run(run_config: str, num_runs: int, data_version: str, log_level: int) -> int:
    """
    Purpose:
        Prepare for magicwand runs
    Args:
        run_config (String): Path to magicwand json
        num_runs (Int): Number of runs
        data_version (String): Folder for runs
        log_level (Int): Log level for run
    Returns:
        status (Int): -1 if fail, 0 if success
    """
    # Create new runner class
    mw_runner = MwRunner(log_level)

    config = mw_runner.pre_run_check(run_config, data_version)

    if config is not None:

        counter = 0
        while counter < num_runs:

            try:
                counter += 1
                run_json, compoents = mw_runner.build_docker_compose(config, log_level)
                if run_json is not None and compoents is not None:
                    mw_runner.start_docker_containers(run_json, config, counter)
                    mw_runner.stop_docker_containers(run_json, counter, data_version)

                    post_run_data = mw_runner.post_run_actions(run_json, data_version)

                    if not bool(post_run_data):
                        mw_runner.logger.error("Failure post run")
                        return -1

                    mw_runner.logger.info(
                        "Running verifications for " + post_run_data["run_loc"]
                    )

                    mw_global = MwGlobal(log_level)
                    compoents.append(mw_global)

                    verify_json = {}
                    for compoent in compoents:
                        passed = compoent.verify(run_json, post_run_data)
                        mw_runner.logger.info(f"{compoent.name} verification {passed}")
                        verify_json[compoent.name] = passed

                    outfilename = post_run_data["run_loc"] + "verify_run.json"
                    try:
                        with open(outfilename, "w") as outfile:
                            json.dump(verify_json, outfile)
                    except Exception as error:
                        mw_runner.logger.error("Run " + str(counter) + " Failed")
                        raise OSError(error)

                else:
                    mw_runner.logger.error("Error during setup")
                    return -1

            except Exception as error:
                mw_runner.logger.error(error)
                return -1
        return 0
    else:
        return -1
