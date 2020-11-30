"""
Purpose:
    This file contains the class for Magicwand Locust

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
import numpy as np  # type: ignore
from collections import Counter

from typing import Any, Dict, Union
from magicwand.magicwand_components.mw_component import MwComponent
from magicwand.magicwand_utils.magicwand_utils import get_logger
from magicwand.magicwand_utils.magicwand_utils import load_json

MAX_IP_THREADS = (
    5  # Maximum number of threads/clients/users that can be assigned to a single IP
)
DIST_SCALE = (
    2  # Scale of the normal distribution for assigning thread/client/user nums to IPs
)


class MwLocust(MwComponent):

    name = "MW_Locust"

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
        self._config = load_json("magicwand_components/benign/mw_locust.json")

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
        if self.config is None:
            return -1

        try:
            os.environ["CURR_CLIENT_DURATION"] = str(
                self.config["client_options"]["client_duration"]
            )
            if "locust_duration" in self.config["client_options"]:
                os.environ["CURR_LOCUST_DURATION"] = str(
                    self.config["client_options"]["locust_duration"]
                )
            else:
                os.environ["CURR_LOCUST_DURATION"] = "NONE"

            if self.config["client_options"].get("seed") is not None:
                # TODO: would be better if we could apply type checking to the config
                # via a schema, as opposed to manually checking individual keys/values.
                curr_seed = str(self.config["client_options"]["seed"])
                os.environ["CURR_SEED"] = curr_seed
                if not curr_seed == "None":
                    np.random.seed(int(os.environ["CURR_SEED"]))
            else:
                os.environ["CURR_SEED"] = "None"

            # Users will only set number of IPs now
            num_ips = int(self.config["client_options"]["num_ips"])
            os.environ["CURR_NUM_IPS"] = str(num_ips)

            # based on number of ips we will set the num_clients and hatch rate

            locust_stats = self.prob_dist_function(num_ips)

            os.environ["CURR_NUM_CLIENTS"] = str(locust_stats["num_clients"])
            os.environ["CURR_HATCH_RATE"] = str(locust_stats["hatch_rate"])

            # hmm dont like this, but lets see how it goes for now
            os.environ["CURR_PROB_DIST"] = str(locust_stats["prob_dist"])

            # Advanced options
            if "keepalive" in self.config["client_options"]:
                os.environ["CURR_KEEPALIVE"] = self.config["client_options"][
                    "keepalive"
                ]
            else:
                os.environ["CURR_KEEPALIVE"] = "ON"

            if "stagger" in self.config["client_options"]:
                os.environ["CURR_STAGGER"] = self.config["client_options"]["stagger"]
            else:
                os.environ["CURR_STAGGER"] = "ON"
            if "wait_max" in self.config["client_options"]:
                os.environ["CURR_WAIT_MAX"] = str(
                    self.config["client_options"]["wait_max"]
                )
            else:
                os.environ["CURR_WAIT_MAX"] = "60"

            if "traffic_behavior" in self.config["client_options"]:
                os.environ["CURR_TRAFFIC_BEHAVIOR"] = self.config["client_options"][
                    "traffic_behavior"
                ]
            else:
                os.environ["CURR_TRAFFIC_BEHAVIOR"] = "default"

            return 0
        except Exception as error:
            self.logger.error(error)
            return -1

    # TODO fill out method
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

    def prob_dist_function(self, num_ips: int) -> Dict[str, Any]:
        """
        Purpose:
            Return probabilistic distribution based on IPs
        Args:
            num_ips: Number of IPS
        Returns:
            prob_dist: The distrbution for the ips
        """
        prob_dist = dict(
            Counter(
                [
                    int(np.ceil(np.abs(np.random.normal(scale=DIST_SCALE))))
                    for _ in range(num_ips)
                ]
            )
        )

        # Limit max threads/clients/users spawned for a single IP
        for num_threads, num_ips in list(prob_dist.items()):
            if num_threads > MAX_IP_THREADS:
                prob_dist[MAX_IP_THREADS] = prob_dist.get(MAX_IP_THREADS, 0) + num_ips
                del prob_dist[num_threads]

        locust_stats: Dict[str, Any] = {}
        locust_stats["prob_dist"] = prob_dist

        # Number of clients will be the sum of each ips threads
        num_clients = 0
        for num_threads, num_ips in prob_dist.items():
            num_clients += num_threads * num_ips
        locust_stats["num_clients"] = num_clients

        # divide num_cleints by 10 to get hatch rate
        locust_stats["hatch_rate"] = max(num_clients // 10, 1)

        return locust_stats
