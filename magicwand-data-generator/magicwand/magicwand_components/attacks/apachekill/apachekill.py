"""
Purpose:
    This file contains the class for Apachekill

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
from typing import Any, Dict, Union, List, Tuple

import pandas as pd  # type: ignore

from magicwand.magicwand_components.mw_component import MwComponent
from magicwand.magicwand_utils.magicwand_utils import get_logger, load_json


class Apachekill(MwComponent):

    name = "Apachekill"
    # We chose the number from our own internal testing, that showed that apachekill
    # packets have a mean size greater than 1500 due to the overlaping range header
    # bytes each packet contains
    attack_length_mean = 1500

    # TODO find better place?
    ratio_json: Dict[str, Any] = {
        "attack": "apachekill",
        "checks": [
            {
                "attack_ratio": 1,
                "client_ratio": 2,
                "diff_higher": "attack",
                "check_type": "rtt_mean",
            },
            {
                "attack_ratio": 1,
                "client_ratio": 1,
                "diff_higher": "attack",
                "check_type": "mem_mean",
            },
            {
                "attack_ratio": 1,
                "client_ratio": 1,
                "diff_higher": "attack",
                "check_type": "total_traffic",
            },
        ],
    }

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
        # self._logger = get_logger("mw-log", log_level)
        super().__init__(log_level=log_level)

        # set config to expected spot
        self._config = load_json("magicwand_components/attacks/apachekill.json")

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
            locust_config = load_json("magicwand_components/benign/mw_locust.json")
            if "seed" in locust_config["client_options"]:
                os.environ["CURR_SEED"] = str(locust_config["client_options"]["seed"])
            else:
                os.environ["CURR_SEED"] = "None"
        except Exception as error:
            print(error)
            print("Failed to load seed from mw_locust.json, defaulting to 'None'")
            os.environ["CURR_SEED"] = "None"
        try:
            attack_options: Dict[str, Any] = self.config["attack_options"]
            os.environ["CURR_ATTACK_DURATION"] = str(attack_options["ak_duration"])
            os.environ["CURR_IP_LIMIT"] = str(attack_options["ak_num_ips"])
            os.environ["CURR_DELAY"] = str(attack_options.get("attack_delay", 15))
            os.environ["CURR_MAX_THREADS"] = str(attack_options["ak_num_threads"])
            return 0
        except Exception as error:

            raise ValueError(
                str(error)
                + " is a required field for apachekill configs, please check the config and return once the error is corrected"
            )

    def get_calibrate_data(self, run_loc: str) -> Dict[str, Any]:
        """
        Purpose:
            Get all data needed for calibrate
        Args:
            run_loc: Where data is located
        Returns:
            calibrate_data: Dict of all data needed
        """
        calibrate_data = {}

        try:
            calibrate_data["mem_df"] = pd.read_csv(run_loc + "mem_stats.csv")
            calibrate_data["apache_df"] = pd.read_csv(run_loc + "apache_stats.csv")
            calibrate_data["rtt_df"] = pd.read_csv(run_loc + "rtt_stats.csv")
            calibrate_data["run_json_loc"] = run_loc + "run_parms.json"
        except Exception as error:
            raise OSError(f"{error}")

        return calibrate_data

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

        ip_map = post_run_data["attack_ips"]
        attack_ips = list(ip_map["ip"])
        tcp_csv = post_run_data["tcpcsv"]

        if len(attack_ips) == 0:
            self.logger.error("No IPs to verify?")
            passed = False

        for ip in attack_ips:

            attack_df = tcp_csv.loc[
                (tcp_csv["_ws.col.Source"] == ip)
                & (tcp_csv["_ws.col.Protocol"] == "HTTP")
            ]

            self.logger.debug("Stats for IP: " + ip)

            # the mean length
            attack_length_mean = attack_df["_ws.col.Length"].mean()

            try:
                if int(attack_length_mean) > self.attack_length_mean:
                    pass
                else:
                    self.logger.error("Fail mean length")
                    self.logger.error(
                        "IP:" + ip + " http length mean: " + str(attack_length_mean)
                    )
                    passed = False
            except Exception as error:
                self.logger.debug(error)
                continue

            # This is the start of the header string, that we need to split off to get the array
            # of values of overlapping bytes
            header_cutoff = "Range: bytes=0-,"
            for index, row in attack_df.iterrows():
                self.logger.debug("Index: " + str(index))

                # Make sure it came from apachekill
                if row["http.user_agent"] == "KillApachePy (0.1c)":
                    pass
                else:
                    # if we limit pcap we wont get user agent so wont check it..
                    self.logger.debug(f"Invalid user-agent: {row['http.user_agent']}")
                    # passed = False

                # Now check the range headers
                try:
                    header_string = (
                        row["http.request.line"]
                        .split(header_cutoff)[1]
                        .replace("\\r\\n,", "")
                        .split("User-Agent:")[0]
                    )
                except Exception as error:
                    self.logger.debug(error)
                    continue
                range_headers = header_string.split(",")

                if not self.range_header_test(range_headers):
                    passed = False

        return passed

    ###
    # Data Validation
    ###

    @classmethod
    def range_header_test(self, range_headers: List[str]) -> bool:
        """
        Purpose:
            To test if apachekill range header overlap exploit is in pcap
        Args:
            range_headers (Array): Array of range headers
        Returns:
            overlapped (Boolean): True if range header overlap is present at least
                75% of the time
        """
        start = True
        overlap = 0
        range_length = len(range_headers)
        overlapped = False
        # In apachekill the ranger headers are a long string that looks like....
        # [1-500],[2-501],[3-502],[4-504],[5-505]....
        # The goal of this function is to see if the range headers overlap
        # i.e 1-500 and 2-501 have overlapping values

        for range_header in range_headers:
            ranger_header = range_header.strip()
            if ranger_header == "":
                continue
            try:
                # the first number in the range header i.e 1-500 will be 1
                range_min = int(ranger_header.split("-")[0])
                # the second number in the range header i.e 1-500 will be 500
                range_max = int(ranger_header.split("-")[1])
            except Exception as error:
                # if we limit pcap we will get a break here
                logging.debug(f"Not a full pcap: {repr(error)}")
                break

            # The first range header we check doesnt have a prev or max,
            # so we set the defaults to current range header min and max, only do this once
            if start:
                prev_max = range_max
                prev_min = range_min
                start = False
                continue

            # check if overlap from previous request
            # if 501 > 500 and 5 <= 5 then overlap +=1 else pass
            if range_max > prev_max and range_min <= prev_min:
                overlap += 1

        # Out of all the requests what is the percentage of overlap
        overlap_percent = float(overlap / range_length)

        # if we have at least 75% overlap then the run "passed" the apachekill test
        if overlap_percent >= 0.75:
            overlapped = True

        return overlapped

    def suggested_threads_ak(self, num_threads: int, status: str) -> int:
        """
        Purpose:
            Suggest number of apachekill threads for next run
        Args:
            num_threads (Int): Number of apachekill threads from last run
            status (String): Status of last attack either Strong or Weak
        Returns:
            use_num_threads (Int): Number of apachekill threads to use in next run
        """
        use_num_threads = 100

        if status == "weak":
            if num_threads < 50:
                use_num_threads = 50
            else:
                use_num_threads = num_threads * 2

        if status == "strong":
            if num_threads > 100:
                use_num_threads = int(num_threads / 2)
            elif num_threads < 10:
                use_num_threads = 1
            else:
                use_num_threads = num_threads - 10

        return use_num_threads

    def ratio_formula(
        self,
        check: Dict[str, Any],
        run_json_attack: Dict[str, Any],
        run_json_benign: Dict[str, Any],
        apache_df: pd.DataFrame,
        apache_df_attack: pd.DataFrame,
        rtt_df: pd.DataFrame,
        rtt_df_attack: pd.DataFrame,
        mem_df: pd.DataFrame,
        mem_df_attack: pd.DataFrame,
    ) -> dict:
        """
        Purpose:
            Evaluate Run based on given ratio formula
        Args:
            check (Dict): Ratio check object example: {"attack_ratio": 1, "client_ratio": 2, "diff_higher": "attack", "check_type": "rtt_mean"}
            run_json_attack: magicwand attack data
            run_json_benign: magicwand benign data
            apache_df (DataFrame): Pandas dataframe of client only run apache stats
            apache_df_attack (DataFrame): Pandas dataframe of attack only run apache stats
            rtt_df (DataFrame): Pandas dataframe of client only run rtt stats
            rtt_df_attack (DataFrame): Pandas dataframe of attack only run rtt stats
            mem_df (DataFrame): Pandas dataframe of client only run memory stats
            mem_df_attack (DataFrame): Pandas dataframe of attack only run memory stats
        Returns:
            checkObj (Dict): Parameters for next run
            check_obj["passed_checks"] (Boolean): If run passed ratio checks
            check_obj["sugg_clients"] = Number of clients to use for next run
            check_obj["sugg_threads"] = Number of attack threads to use for next run
        """
        attack = "apachekill"
        curr_client_threads = int(
            run_json_benign["benign"]["client_options"]["num_ips"]
        )

        total_traffic_values = apache_df["total_traffic"][-1:].values[0].split(" ")

        total_traffic_attack_values = (
            apache_df_attack["total_traffic"][-1:].values[0].split(" ")
        )

        # check client vs attack
        total_traffic_client_bytes: float = 0.0
        total_traffic_attack_bytes: float = 0.0

        if total_traffic_values[1] == "kB":
            total_traffic_client_bytes = float(total_traffic_values[0]) / 1000

        if total_traffic_values[1] == "MB":
            total_traffic_client_bytes = float(total_traffic_values[0])

        if total_traffic_values[1] == "GB":
            total_traffic_client_bytes = float(total_traffic_values[0]) * 1000

        if total_traffic_attack_values[1] == "kB":
            total_traffic_attack_bytes = float(total_traffic_attack_values[0]) / 1000

        if total_traffic_attack_values[1] == "MB":
            total_traffic_attack_bytes = float(total_traffic_attack_values[0])

        if total_traffic_attack_values[1] == "GB":
            total_traffic_attack_bytes = float(total_traffic_attack_values[0]) * 1000

        check_obj: Dict[str, Any] = {}
        passed_checks = True
        check_obj["passed_checks"] = True

        client_ratio = check["client_ratio"]
        attack_ratio = check["attack_ratio"]

        if attack == "apachekill":

            self.logger.debug("checking apachekill")

            if check["check_type"] == "rtt_mean":
                # Check to see if the rtt mean for attack is higher than benign

                rtt_mean = float(rtt_df.describe()["rtt"]["mean"])
                rtt_attack_mean = float(rtt_df_attack.describe()["rtt"]["mean"])

                if check["diff_higher"] == "attack":

                    if rtt_mean * int(client_ratio) < rtt_attack_mean * int(
                        attack_ratio
                    ):
                        self.logger.debug("Attack is good")
                        pass
                    else:
                        self.logger.debug("attack is weak rtt")
                        if curr_client_threads < 20:
                            sugg_clients = 20
                        else:
                            sugg_clients = int(curr_client_threads * 2)

                        sugg_threads = self.suggested_threads_ak(
                            run_json_attack["attack"]["attack_options"][
                                "ak_num_threads"
                            ],
                            "weak",
                        )
                        passed_checks = False
                        self.logger.debug("tunning attack")
                        check_obj["max_clients"] = (
                            int(run_json_attack["sut"]["max_clients"]) * 2
                        )

                if check["diff_higher"] == "client":

                    if rtt_mean * int(client_ratio) > rtt_attack_mean * int(
                        attack_ratio
                    ):
                        self.logger.debug("Client is good")

                    else:
                        if curr_client_threads < 20:
                            sugg_clients = 20
                        else:
                            sugg_clients = int(curr_client_threads * 2)
                        sugg_threads = self.suggested_threads_ak(
                            run_json_attack["attack"]["attack_options"][
                                "ak_num_threads"
                            ],
                            "strong",
                        )
                        passed_checks = False
                        check_obj["max_clients"] = int(
                            run_json_attack["sut"]["max_clients"]
                        )

                if not passed_checks:
                    check_obj["passed_checks"] = False
                    check_obj["sugg_clients"] = sugg_clients
                    check_obj["sugg_threads"] = sugg_threads
                    return check_obj

            if check["check_type"] == "mem_mean":
                # Check to see if the memory mean for attack is higher than benign

                mem_mean = mem_df["memory_percent"].mean()
                mem_attack_mean = mem_df_attack["memory_percent"].mean()

                self.logger.debug("checking memory")

                if check["diff_higher"] == "attack":

                    if mem_mean * int(client_ratio) < mem_attack_mean * int(
                        attack_ratio
                    ):
                        self.logger.debug("Attack is good")
                        pass
                    else:
                        self.logger.debug("attack is weak mem")
                        if curr_client_threads < 20:
                            sugg_clients = 20
                        else:
                            sugg_clients = int(curr_client_threads * 2)

                        sugg_threads = self.suggested_threads_ak(
                            run_json_attack["attack"]["attack_options"][
                                "ak_num_threads"
                            ],
                            "weak",
                        )
                        passed_checks = False
                        check_obj["max_clients"] = (
                            int(run_json_attack["sut"]["max_clients"]) * 2
                        )

                if check["diff_higher"] == "client":

                    if mem_mean * int(client_ratio) > mem_attack_mean * int(
                        attack_ratio
                    ):
                        self.logger.debug("Client is good")

                    else:
                        if curr_client_threads < 20:
                            sugg_clients = 20
                        else:
                            sugg_clients = int(curr_client_threads * 2)
                        sugg_threads = self.suggested_threads_ak(
                            run_json_attack["attack"]["attack_options"][
                                "ak_num_threads"
                            ],
                            "strong",
                        )
                        passed_checks = False
                        check_obj["max_clients"] = int(
                            run_json_attack["sut"]["max_clients"]
                        )

                if not passed_checks:
                    check_obj["passed_checks"] = False
                    check_obj["sugg_clients"] = sugg_clients
                    check_obj["sugg_threads"] = sugg_threads
                    return check_obj

            if check["check_type"] == "total_traffic":
                # Check to see if the traffic mean for attack is higher than benign

                self.logger.debug("checking traffic")
                if check["diff_higher"] == "attack":

                    if total_traffic_client_bytes * int(
                        client_ratio
                    ) < total_traffic_attack_bytes * int(attack_ratio):
                        self.logger.debug("Attack is good")
                        pass
                    else:
                        self.logger.debug("attack is weak traffic")
                        sugg_clients = int(curr_client_threads / 2)

                        sugg_threads = self.suggested_threads_ak(
                            run_json_attack["attack"]["attack_options"][
                                "ak_num_threads"
                            ],
                            "weak",
                        )
                        passed_checks = False
                        check_obj["max_clients"] = (
                            int(run_json_attack["sut"]["max_clients"]) * 2
                        )

                if check["diff_higher"] == "client":

                    if total_traffic_client_bytes * int(
                        client_ratio
                    ) > total_traffic_attack_bytes * int(attack_ratio):
                        self.logger.debug("Client is good")

                    else:
                        self.logger.debug("attack sent too much traffic")
                        if curr_client_threads < 20:
                            sugg_clients = 20
                        else:
                            sugg_clients = int(curr_client_threads * 2)
                        sugg_threads = self.suggested_threads_ak(
                            run_json_attack["attack"]["attack_options"][
                                "ak_num_threads"
                            ],
                            "strong",
                        )
                        passed_checks = False
                        check_obj["max_clients"] = int(
                            run_json_attack["sut"]["max_clients"]
                        )

                if not passed_checks:
                    check_obj["passed_checks"] = False
                    check_obj["sugg_clients"] = sugg_clients
                    check_obj["sugg_threads"] = sugg_threads
                    return check_obj

        return check_obj

    def ratio_checker(
        self,
        run_json_attack: Dict[str, Any],
        run_json_benign: Dict[str, Any],
        apache_df: pd.DataFrame,
        apache_df_attack: pd.DataFrame,
        rtt_df: pd.DataFrame,
        rtt_df_attack: pd.DataFrame,
        mem_df: pd.DataFrame,
        mem_df_attack: pd.DataFrame,
    ) -> Tuple[bool, Dict[str, Any], Dict[str, Any]]:
        """
        Purpose:
            Prepare ratio check for the run
        Args:
            run_json_attack: magicwand attack data
            run_json_benign: magicwand benign data
            apache_df (DataFrame): Pandas dataframe of client only run apache stats
            apache_df_attack (DataFrame): Pandas dataframe of attack only run apache stats
            rtt_df (DataFrame): Pandas dataframe of client only run rtt stats
            rtt_df_attack (DataFrame): Pandas dataframe of attack only run rtt stats
            mem_df (DataFrame): Pandas dataframe of client only run memory stats
            mem_df_attack (DataFrame): Pandas dataframe of attack only run memory stats
        Returns:
            passed_checks: True if passed, else False
            run_json_attack: New attack config
            run_json_benign: New benign config
        """
        self.logger.debug("Checking ratio")
        passed_checks = True

        self.logger.debug(self.ratio_json["checks"])

        for check in self.ratio_json["checks"]:

            try:
                check_obj = self.ratio_formula(
                    check,
                    run_json_attack,
                    run_json_benign,
                    apache_df,
                    apache_df_attack,
                    rtt_df,
                    rtt_df_attack,
                    mem_df,
                    mem_df_attack,
                )
            except Exception as error:
                self.logger.error(error)
                raise OSError("Problem with checking ratio...")

            if not check_obj["passed_checks"]:
                passed_checks = False
                break

        self.logger.info("Checking results...")
        self.logger.debug(passed_checks)
        if passed_checks:
            run_json_attack["sut"]["run_duration"] = 300
            self.logger.info("Calibration Completed Successfully")
            return passed_checks, run_json_attack, run_json_benign

        else:
            run_json_benign["benign"]["client_options"]["num_ips"] = check_obj[
                "sugg_clients"
            ]
            run_json_attack["attack"]["attack_options"]["ak_num_threads"] = check_obj[
                "sugg_threads"
            ]
            run_json_attack["sut"]["max_clients"] = check_obj["max_clients"]
            run_json_benign["sut"]["max_clients"] = check_obj["max_clients"]

            self.logger.info("Re running for 5 minutes")
            return passed_checks, run_json_attack, run_json_benign
