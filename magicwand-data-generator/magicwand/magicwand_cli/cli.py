#!/usr/bin/env python3
"""
Purpose:
    Entrypoint script for MAGICWAND. Is the CLI interface for ...

Steps:
    - Init CLI command and froups

Script Call:
    magicwand COMMAND [ARGS]...

Example Call:
    magicwand --help

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
import os
import sys
import logging
import click

# Local Python Library Imports
from magicwand.magicwand_state.magicwand_state import MagicwandState
from magicwand.magicwand_utils import (
    magicwand_utils,
    start_runs,
    init_utils,
)
import magicwand.magicwand_components.mw_calibrate as mw_calibrate


# Setup Magicwand Logging
LOGLEVEL = logging.INFO
logging.basicConfig(
    format="%(asctime)s | %(levelname)s : %(message)s",
    level=LOGLEVEL,
    stream=sys.stdout,
)
LOGGER = logging.getLogger("mw-log")


###
# Globals
###

MagicwandConfig = magicwand_utils.load_configs()


def check_if_in_project() -> bool:
    """
    Purpose:
       Prepare magicwand for calibration

       # SKIP, this should be in a util and prob should be called
    Args:
        N/A
    Returns:
        status (Boolean): False if not in magicwand project, True if in magicwand project
    """
    # check if folder exisit
    if os.path.exists(".mw_proj"):
        # SKIP we should only check this file, in a git project if you delete .git
        # you are no longer in a git project we will follow that example
        status = True
    else:
        LOGGER.info("Not inside Magicwand Project")
        LOGGER.info("run `magicwand init --folder=FOLDER_NAME` and retry")
        status = False
    return status


def _get_log_level(verbose: bool) -> int:
    """
    Purpose:
        Get the log level
    Args:
        verbose (bool): log with verbose enabled
    Returns:
        int: the log level
    """
    return logging.DEBUG if verbose else logging.INFO


###
# CLI Entrypoint
###


@click.group(invoke_without_command=False)
@click.version_option(MagicwandConfig.VERSION)
@click.pass_context
def magicwand_cli(cli_context: click.Context) -> None:
    """Magicwand data generation tool"""
    """
    Purpose:
        Magicwand entrypoint command
    Args:
        cli_context( Object )- cli object for magicwand
    Returns:
        N/A
    """

    # Get context about the command being run (which Click had a better
    # way to do this)
    # cli_command = " ".join(sys.argv[:])
    # command_root = cli_context.command_path
    # command_subcommand = cli_context.invoked_subcommand

    cli_context.obj = MagicwandState()


###
# Magicwand Commands
###


@click.command("calibrate")
@click.option("--ratio", help="Ratio config file", required=False)
@click.option("--verbose", "-v", is_flag=True, help="Print more output.")
@click.option(
    "--attack",
    default="apachekill",
    help="Attack to tune, valid options: apachekill",
    required=True,
)
def calibrate_command(attack: str, ratio: str, verbose: str) -> None:
    """Calibrate the magicwand tool"""
    """
    Purpose:
        Calibrate magicwand
    Args:
        attack (String) - attack to calibrate
        ratio (String) - ratio config file 
        verbose (Boolean) - Print debug messages
    Returns:
        N/A
    """
    if not check_if_in_project():
        sys.exit(1)

    LOGGER.info("Running calibration for: " + attack)
    try:
        if mw_calibrate.calibrate(attack, _get_log_level(verbose)) != 0:
            sys.exit(1)
    except ValueError as error:
        LOGGER.exception(error)
        sys.exit(1)
    except OSError as error:
        LOGGER.fatal(error)
        sys.exit(1)
    except Exception as error:
        LOGGER.fatal(error)
        sys.exit(1)

    LOGGER.info("Calibration Process Finished")


@click.command("run")
@click.option("--config", help="JSON file with run parameters", required=True)
@click.option(
    "--data_version", default="test_runs", help="Folder to save runs", required=True
)
@click.option("--count", default=1, help="Number of runs", type=int)
@click.option("--verbose", "-v", is_flag=True, help="Print more output.")
def run_command(config: str, count: int, data_version: str, verbose: bool) -> None:
    """Start a run to generate data"""
    """
    Purpose:
        Start a run to generate data
    Args:
        config(String) - JSON file with run parameters
        count(Int) - Number of runs
        data_version(string) - Folder to save runs
        verbose(Boolean) - Print debug messages
    Returns:
        N/A
    """
    if not check_if_in_project():
        sys.exit(1)

    if start_runs.run(config, count, data_version, _get_log_level(verbose)) != 0:
        sys.exit(1)

    LOGGER.info("Run Process Finished")


@click.command("init")
@click.option("--project", help="Project to create", required=True)
def init_command(project: str) -> None:
    """Create and initialize magicwand folder"""
    """
    Purpose:
        Create and initialize magicwand folder
    Args:
        folder (String) - Folder to create
    Returns:
        N/A
    """
    # already pevents duplicate inits
    # No force let them delete their data

    if init_utils.init(project) != 0:
        sys.exit(1)


@click.command("convert")
@click.option("--pcap", help="PCAP to convert", required=True)
@click.option("--output", "-o", default="cic_flow.csv", help="Output .csv filename")
@click.option(
    "--force",
    "-f",
    is_flag=True,
    default=False,
    help="Force output file to be overwritten if it already exists.",
)
def convert_command(pcap: str, output: str, force: bool) -> None:
    """Convert any pcap file to a CIC csv file"""
    """
    Purpose:
        Convert any pcap file to a CIC csv file
    Args:
        pcap (String) - Name of the pcap file to convert
        output (String) - Name of output file
        force (flag) - Overwrite file if exists
    Returns:
        N/A
    """

    if magicwand_utils.convert_pcap(pcap, output, force) != 0:
        sys.exit(1)


###
# CLI Startup
###


def setup_magicwand_cli() -> None:
    """
    Purpose:
        Build Command Groups for Magicwand CLI.
    Args:
        N/A
    Returns:
        N/A
    """

    # Magicwand Commands
    magicwand_cli.add_command(init_command)
    magicwand_cli.add_command(calibrate_command)
    magicwand_cli.add_command(run_command)
    magicwand_cli.add_command(convert_command)


###
# Script Main Execution
###


if __name__ == "__main__":

    try:
        setup_magicwand_cli()
    except Exception as err:
        print(f"{os.path.basename(__file__)} failed due to error: {err}")
        raise err
