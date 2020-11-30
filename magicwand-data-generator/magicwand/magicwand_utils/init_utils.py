# mypy: ignore-errors
"""
Purpose:
    This file contains the logic to create a magicwand project

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
import glob
import logging
import os
from pathlib import Path
from shutil import copy

# Local Python Library Imports
from magicwand.magicwand_utils.magicwand_utils import get_logger

###
# Utils
###


def init(folder: str) -> int:
    """
    Purpose:
        Create Magicwand Project
    Args:
        folder (String): Name of Magicwand Project
    Returns:
        status (Int): -1 if fail, 0 if success
    """

    # Set up logger
    try:
        LOGGER = get_logger("mw-log", logging.INFO)
    except Exception as error:
        print(error)
        print("Logging failed?")
        return -1
    # check if folder exists
    if os.path.exists(folder):
        LOGGER.error(folder + " already exists")
        return -1
    else:
        os.mkdir(folder)

    # next make folders we need
    try:
        os.mkdir(folder + "/data_runs")
        os.mkdir(folder + "/configs")
        os.mkdir(folder + "/magicwand_components")
    except Exception as error:
        LOGGER.error(error)
        LOGGER.error("Error making directories")
        return -1

    # make a mw_proj file to indicate we are in a project
    try:
        Path(folder + "/.mw_proj").touch()
    except Exception as error:
        LOGGER.error(error)
        LOGGER.error("Error making project file")
        return -1

    # base dir
    basedir = os.path.dirname(__file__) + "/static_files/"

    # magicwand_components dir
    mw_comp_dir = os.path.dirname(__file__) + "/../magicwand_components/"

    # copy folders
    folders = ["attacks/", "benign/", "sensors/", "suts/"]

    for mw_folder in folders:
        mw_dest = folder + "/magicwand_components/" + mw_folder
        os.mkdir(mw_dest)
        files_to_json = glob.glob(mw_comp_dir + mw_folder + "/*/*.json")
        files_to_yml = glob.glob(mw_comp_dir + mw_folder + "/*/*.yml")

        # LOGGER.info(files_to_json)

        files_to_copy = files_to_json + files_to_yml
        # LOGGER.info(files_to_copy)

        for mw_file in files_to_copy:
            try:
                copy(mw_file, mw_dest)
            except Exception as error:
                LOGGER.error(error)
                LOGGER.error("Error copying " + mw_file)
                return -1

    # copy folders
    folders = ["configs/"]

    for mw_folder in folders:
        mw_dest = folder + "/" + mw_folder
        files_to_copy = glob.glob(basedir + mw_folder + "*")

        for mw_file in files_to_copy:
            try:
                copy(mw_file, mw_dest)
            except Exception as error:
                LOGGER.error(error)
                LOGGER.error("Error copying " + mw_file)
                return -1

    LOGGER.info(f"Magicwand project {folder} created")
    return 0
