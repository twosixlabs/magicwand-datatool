"""
Purpose:
    This file contains the class for magicwand components.

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
from abc import ABC, abstractmethod
from typing import Any, Dict, Union
import logging

from magicwand.magicwand_utils.magicwand_utils import get_logger


class MwComponent(ABC):

    name = "MwComponent"

    def __init__(self, log_level: int):
        """
        Purpose:
            Init MwComponent class
        Args:
            log_level: How verbose to log
        Returns:
            self: MwComponent
        """
        self.logger = get_logger("mw-log", log_level)
        pass

    def __repr__(self) -> str:
        """
        Purpose:
            Representation of the MwComponent object.
        Args:
            N/A
        Returns:
            MwComponent (String): String representation of MwComponent
        """

        return f"<MwComponent {self.name}>"

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
        pass

    @config.setter  # type: ignore
    @abstractmethod
    def config(self, val: Dict[str, Any]) -> None:
        """
        Purpose:
            Set config
        Args:
            val: value of the config
        Returns:
            N/A
        """
        pass

    @abstractmethod
    def set_env_variables(self) -> int:
        """
        Purpose:
            Set environment variables
        Args:
            N/A
        Returns:
            stats: 0 if worked, -1 if failed
        """
        pass

    @abstractmethod
    def verify(self, config: Dict[str, Any], post_run_data: Dict[str, Any]) -> bool:
        """
        Purpose:
            Verify the component
        Args:
            config: Run config options
            post_run_data: Data for verifications
        Returns:
            passed: If verfication passed or failed
        """
        pass

    def get_calibrate_data(self, run_loc: str) -> Dict[str, Any]:
        """
        Purpose:
            Get all data needed for calibrate
        Args:
            run_loc: Where data is located
        Returns:
            calibrate_data: Dict of all data needed
        """
        pass
