"""
Purpose:
    This file contains the class for MwGlobal

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

import pandas as pd  # type: ignore
from magicwand.magicwand_components.mw_component import MwComponent
from magicwand.magicwand_utils.magicwand_utils import get_logger


class MwGlobal(MwComponent):

    name = "MW_Global"

    def __init__(self, log_level=logging.INFO) -> None:
        """
        Purpose:
            Init Component
        Args:
            log_level: Verbosity of the logger
        Returns:
            self: The MwComponent
        """
        # get logger
        # self._logger = get_logger("mw-log", log_level)
        super().__init__(log_level=log_level)
        # place holder config
        self._config = {"global": "mw_global"}

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
    def config(self, val: Dict[str, Any]):
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
        # TODO make timeout a config var
        return 0

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
        passed = True
        ip_map = post_run_data["ip_map"]
        tcp_csv = post_run_data["tcpcsv"]

        if not self.verify_all_expected_ips_in_pcap(ip_map, tcp_csv, self.logger):
            passed = False

        if not self.verify_no_unexpected_ips_in_pcap(ip_map, tcp_csv, self.logger):
            passed = False

        return passed

    def verify_no_unexpected_ips_in_pcap(
        self, ip_map: pd.DataFrame, tcpcsv: pd.DataFrame, logger: logging.Logger
    ) -> bool:
        """
        Purpose:
            To test for unexpected IP addresses are in the resulting PCAP.
            Compare IPs from the configs to the PCAP and list unexpected.
        Args:
            ip_map (Dataframe): Dataframe of ips
            tcpsv (Dataframe): Dataframe of run pcap
            logger: The logger object
        Returns:
            passed (Boolean): True if the IPs are in the run
        """
        all_ips = list(ip_map["ip"])
        tcp_ips = set(list(tcpcsv["_ws.col.Source"]))
        passed = True

        if len(all_ips) == 0 or len(tcp_ips) == 0:
            logging.error("NO IPs to check?")
            return False

        # Make sure all tcpdump ips are in ip_map
        for ip in tcp_ips:
            if ip in all_ips:
                continue
            # check to make sure not a MAC address/ARP packet
            elif ":" in ip:
                continue
            else:
                logger.error("IP:" + ip + " is unexpected")
                passed = False

        return passed

    def verify_all_expected_ips_in_pcap(
        self, ip_map: pd.DataFrame, tcpcsv: pd.DataFrame, logger: logging.Logger
    ) -> bool:
        """
        Purpose:
            To test if we all expected IPs from the experiment configuration are in the PCAP
        Args:
            ip_map (Dataframe): Dataframe of ips
            tcpsv (Dataframe): Dataframe of run pcap
            logger: The logger object
        Returns:
            passed (Boolean): True if the IPs are in the run
        """
        all_ips = list(ip_map["ip"])

        tcp_ips = set(list(tcpcsv["_ws.col.Source"]))

        # check if all ips are present
        passed = True

        # TODO rework this for attempted to reach
        for ip in all_ips:
            if ip in tcp_ips:
                logger.debug("IP:" + ip + " is in tcpdump")
            else:
                logger.warning("IP:" + ip + " is not in tcpdump")
                # passed = False
        # result is not saved anywhere
        return passed
