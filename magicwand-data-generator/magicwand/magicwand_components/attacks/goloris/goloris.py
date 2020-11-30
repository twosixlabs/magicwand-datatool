"""
Purpose:
    This file contains the class for Goloris

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
import logging
import os
import time
from typing import Any, Dict, Union, List


from magicwand.magicwand_components.mw_component import MwComponent
from magicwand.magicwand_utils.magicwand_utils import load_json


class Goloris(MwComponent):

    name = "Goloris"

    def __init__(self, log_level: int = logging.INFO) -> None:
        """
        Purpose:
            Init Component
        Args:
            log_level: Verbosity of the logger
        Returns:
            self: The MwComponent
        """
        # get logger
        super().__init__(log_level=log_level)

        # set config to expected spot
        self._config = load_json("magicwand_components/attacks/goloris.json")

    @property
    def config(self) -> Dict[str, Any]:
        """
        Purpose:
            Get config
        Args:
            N/A
        Returns:
            config: The json config for the component
        """
        return self._config

    @config.setter
    def config(self, val: Dict[str, Any]) -> None:
        """
        Purpose:
            Set config
        Args:
            val: value of the config
        Returns:
            N/A
        """
        self.config = val

    def set_env_variables(self) -> int:
        """
        Purpose:
            Set environment variables
        Args:
            N/A
        Returns:
            stats: 0 if worked, -1 if failed
        """

        try:
            attack_options: Dict[str, Any] = self.config["attack_options"]
            os.environ["CURR_ATTACK_DURATION"] = str(attack_options["attack_duration"])
            os.environ["CURR_WORKER_COUNT"] = str(attack_options["worker_count"])
            os.environ["CURR_RAMP_UP_INTERVAL"] = str(
                attack_options["ramp_up_interval"]
            )
            os.environ["CURR_DELAY"] = str(attack_options.get("attack_delay", 15))
            return 0
        except Exception as error:

            raise ValueError(
                str(error)
                + " is a required field for Goloris configs, please check the config and return once the error is corrected"
            )

    def verify(self, config: Dict[str, Any], post_run_data: Dict[str, Any]) -> bool:
        """
        Purpose:
            Verify if the component worked during the run
        Args:
            config: Run config options
            post_run_data: Data for verifications
        Returns:
            passed: True if passed, False if failed
        """
        return True
