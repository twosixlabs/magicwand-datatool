#!/usr/bin/env python3
"""
Purpose:
    MAGICWAND Utilities.

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
import logging
import os
import json
from subprocess import Popen
from typing import Type, Union, Dict, Any

# Local Python Library Imports
from magicwand.magicwand_config.config import Config


###
# Global Configs Functionality
###


CIC_CONVERTER_DOCKER_IMAGE = "twosixlabsmagicwand/mw-cic-converter"


def get_logger(name: str, log_level: int) -> logging.Logger:
    """
    Purpose:
        Load logger object
    Args:
        name (String): name of log
        log_level(Int): Level for log
    Returns:
        logger (Logger obj): Logger object
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Prevent logging from propagating to the root logger
        logger.propagate = False
        console = logging.StreamHandler()
        logger.addHandler(console)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s -  %(name)s - %(message)s"
        )
        console.setFormatter(formatter)
        logger.setLevel(log_level)
    return logger


def load_json(path_to_json: str) -> Dict[str, Any]:
    """
    Purpose:
        Load json files
    Args:
        path_to_json (String): Path to  json file
    Returns:
        Conf: JSON file if loaded, else None
    """
    try:
        with open(path_to_json, "r") as config_file:
            conf = json.load(config_file)
            return conf

    except Exception as error:
        logging.error(error)
        raise TypeError("Invalid JSON file")


def save_json(json_path: str, json_data: Any) -> None:
    """
    Purpose:
        Save json files
    Args:
        path_to_json (String): Path to  json file
        json_data: Data to save
    Returns:
        N/A
    """
    # save sut config
    try:
        with open(json_path, "w") as outfile:
            json.dump(json_data, outfile)
    except Exception as error:
        raise OSError(error)


def load_configs() -> Type[Config]:
    """
    Purpose:
        Load configuration object
    Args:
        environment (String): Environment to get configs for
    Returns:
        config (Config obj): Configuration object
    """

    return Config


def convert_pcap(pcap: str, output: str, force: bool) -> int:
    """
    Purpose:
        Run docker container to convert pcap to CIC csv
    Args:
        pcap (String): Name of the pcap file to be converted
        output (String): Name of the new converted csv file
        force (Bool): Overwrite output if true
    Returns:
        status (Int): -1 on conversion failure, 0 on success
    """
    LOGGER = get_logger("mw-log", logging.INFO)

    if not os.path.exists(pcap):
        LOGGER.error(f"Cannot find pcap file {pcap}")
        return -1

    pcap_folder_location = os.path.dirname(os.path.abspath(pcap))
    pcap_filename = os.path.basename(pcap)

    # If the user hasn't specified an output path, use the input pcap dir
    if "/" not in output or output == "cic_flow.csv":
        output = pcap_folder_location + "/" + output
    if not force and os.path.exists(output):
        LOGGER.info(f"Output file {output} already exists, use convert -f to overwrite")
        return -1

    cmd = f"docker run --rm -v {pcap_folder_location}:/home {CIC_CONVERTER_DOCKER_IMAGE} ./convert_pcap.sh --input={pcap_filename}"
    status = Popen(cmd, shell=True).wait()
    if status != 0:
        LOGGER.error(f"Failed to convert pcap: {pcap}")
        return -1

    # check if file exists
    if not os.path.exists(f"{pcap}_Flow.csv"):
        LOGGER.error(f"Failed to convert pcap: {pcap}")
        return -1

    # Rename output file
    LOGGER.info(f"Moving output file to {output}")
    status = Popen(f"mv -f {pcap}_Flow.csv {output}", shell=True).wait()
    if status != 0:
        LOGGER.error(f"Failed to move csv to {output}")
        return -1

    return status
