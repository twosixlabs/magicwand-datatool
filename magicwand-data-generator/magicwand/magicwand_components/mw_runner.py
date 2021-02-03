"""
Purpose:
    This file contains the logic to run magicwand experiments.

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
from typing import Any, Dict, Union, Mapping, Type, Tuple, List
import pandas as pd  # type: ignore

from magicwand.magicwand_components.attacks import *
from magicwand.magicwand_components.benign import *
from magicwand.magicwand_components.sensors import *
from magicwand.magicwand_components.suts import *
from magicwand.magicwand_components.mw_global import *
from magicwand.magicwand_utils.magicwand_utils import (
    get_logger,
    CIC_CONVERTER_DOCKER_IMAGE,
)
from magicwand.magicwand_config.config import Config

mw_components: Mapping[str, Type[MwComponent]] = {
    "apachekill": Apachekill,
    "sockstress": Sockstress,
    "goloris": Goloris,
    "sht_rudeadyet": Sht_rudeadyet,
    "sht_slowread": Sht_slowread,
    "sht_slowloris": Sht_slowloris,
    "httpflood": Httpflood,
    "synflood": Synflood,
    "mw_locust": MwLocust,
    "mw_rtt_sensor": MwRttSensor,
    "mw_apache_wp": MwApacheWp,
}

valid_values = {
    "attack": [
        "apachekill",
        "sockstress",
        "goloris",
        "sht_rudeadyet",
        "sht_slowread",
        "sht_slowloris",
        "httpflood",
        "synflood",
    ],
    "benign": ["mw_locust"],
    "sut": ["mw_apache_wp"],
    "rtt": ["mw_rtt_sensor"],
}


def signal_handler(run_json: Dict[str, Any], sig: Any, frame: partial) -> Any:
    """
    Purpose:
        Catch Ctrl+C handler
    Args:
        run_json (String): Path to magicwand json
        sig (Object): Signal Object
        frame (Object): Frame Object
    Returns:
        status (Int): -1 if fail, 0 if success
    """
    logging.info("You pressed Ctrl+C! Shutting down gracefully")

    compose_file_string = run_json["compose_file_string"]
    cmd = "docker-compose " + compose_file_string + " down"
    status = os.system(cmd)

    if status != 0:
        logging.error("docker-compose failed")
        sys.exit(-1)

    logging.info("Run Canceled")
    sys.exit(0)


def print_flow_split(cic_data: pd.DataFrame, logger: logging.Logger) -> None:
    """
    Purpose:
        Print out cic flow split
    Args:
        cic_data: Dataframe of the cic data
        logger: MW Runner logger
    Returns:
        N/A
    """
    # Print out attack benign split for each run
    num_total = cic_data.shape[0]
    num_benign = cic_data.loc[cic_data["Label"] == "client"].shape[0]
    num_attacks = cic_data.loc[cic_data["Label"] == "attack"].shape[0]

    num_benign_percent = round(float(num_benign / num_total), 2)
    num_attacks_percent = round(float(num_attacks / num_total), 2)

    logger.info("Benign Stats:")
    logger.info(f"{num_benign} flows out of {num_total} flows: {num_benign_percent}")

    logger.info("Attack Stats:")
    logger.info(f"{num_attacks} flows out of {num_total} flows: {num_attacks_percent}")


def label_cic(row: Dict[str, Any], attr_map: pd.DataFrame) -> str:
    """
    Purpose:
        Get label for cic dataset
    Args:
        row: Dict of values for the CIC flow
        attr_map: Dataframe object of the IPs
    Returns:
        Label: Label for the IP
    """
    src_ip = row["Src IP"]
    dst_ip = row["Dst IP"]
    # find row in attr_map with src_ip
    # check if ip exists
    ip_val = ""

    try:
        ip_val = attr_map.loc[attr_map["ip"] == src_ip]["type"].values[0]

        # if ipval is sut check the dst
        if ip_val == "sut":
            ip_val = attr_map.loc[attr_map["ip"] == dst_ip]["type"].values[0]
    except Exception as error:
        logging.debug(error)
        logging.debug("IP " + src_ip + " not in attr map?")
        ip_val = "unknown"

    return ip_val


def mw_prep_compoent(
    compoent: str, run_json: Dict[str, Any], mw_run_json: Dict[str, Any], log_level: int
) -> Union[MwComponent, None]:
    """
    Purpose:
       Setup run environment variables
    Args:
        curr: Current Compoent
        run_json: Magicwand run level variables
        mw_run_json: Magicwand compoent level variables
    Returns:
        compose_file_string : compose_file_string to use for compoent
    """

    if compoent in run_json:
        current_compoent_string = run_json[compoent]
    else:
        logging.error(compoent + " not in JSON")
        return None

    try:
        current_compoent = mw_components[current_compoent_string](log_level)
        mw_run_json[compoent] = current_compoent.config

    except Exception as error:
        raise ValueError(
            f"{current_compoent_string} is not a valid value for {compoent}.\n Valid values: {valid_values[compoent]}"
        )
    # just return compoents so we can use later
    return current_compoent


def mem_stats(run_loc: str, run_duration: int) -> int:
    """
    Purpose:
       Start docker-stats to calculate memory
    Args:
        run_loc: Where run is located
        run_duration: How long run is going for
    Returns:
        status : 0 if passed, -1 if fail
    """
    # write mem_stats
    cmd = 'echo "timestamp,memory_percent" >>' + run_loc + "mem_stats.csv"
    status = os.system(cmd)

    if status != 0:
        logging.error("echo failed")

    start = time.time()

    while True:
        cmd = "docker stats --no-stream | grep mw-sut-apachewp | awk '{print $7}'"

        try:
            mem_percent_raw = os.popen(cmd).read().split("\n")[0]
        except Exception as warning:
            logging.warning(warning)
            logging.warning("docker-stats failed")
            return -1
        try:
            mem_percent = float(mem_percent_raw[:-1])
        except Exception as warning:
            logging.warning(warning)
            logging.warning("docker-stats failed")
            return -1

        elapsed = round(time.time() - start)

        # write to file
        filename = run_loc + "mem_stats.csv"
        curr_file = open(filename, "a")
        curr_file.write(str(elapsed) + "," + str(mem_percent) + "\n")

        time.sleep(5)

        if elapsed >= run_duration:
            break

    return 0


def run_tshark(run_loc: str) -> int:
    """
    Purpose:
        Run tshark on a PCAP to get the CSV version of the PCAP
    Args:
        run_loc: Location of PCAP file
    Returns:
        status: 0 if passed, -1 if failed
    """
    cmd = (
        "tshark -r "
        + run_loc
        + "tcpdump.pcap -i wlan1 -T fields -E header=y -E separator=, -E quote=d -e _ws.col.No. -e _ws.col.Time -e _ws.col.Source -e _ws.col.Destination -e _ws.col.Protocol -e _ws.col.Length -e _ws.col.Info  -e http.user_agent -e http.connection -e http.request -e http.request.line > "
        + run_loc
        + "tcpdump_verify.csv"
    )
    status = os.system(cmd)

    if status != 0:
        return -1

    return 0


class MwRunner(object):
    def __init__(self, log_level: int):
        """
        Purpose:
            Init MwRunner class
        Args:
            log_level: How verbose the logger should be
        Returns:
            self: MwRunner Class
        """
        # get logger
        self.logger = get_logger("mw-log", log_level)

    def pre_run_check(self, config: str, data_version: str) -> Dict[str, Any]:
        """
        Purpose:
            Do prerun checks
        Args:
            config: the location of config file
            data_version: Where to save the data
        Returns:
            conf: The json config
        """
        # load run config
        conf = load_json(config)
        self.logger.info("Starting runs for data version: " + data_version)

        # check if path exists
        if not os.path.exists("data_runs/" + data_version):

            try:
                os.mkdir("data_runs/" + data_version)
            except Exception as error:
                self.logger.error("Run Failed")
                raise OSError(error)

        return conf

    def build_docker_compose(
        self, config: Dict[str, Any], log_level: int
    ) -> Tuple[Dict[str, Any], List[MwComponent]]:
        """
        Purpose:
            Prepare docker compose
        Args:
            config: The run config json
            log_level: How verbose the logging should be
        Returns:
            mw_run_json, compoents: The run parameters config, and the componets in the run
        """
        curr_time = datetime.datetime.now().strftime("%m_%d_%YT%H_%M_%SZ")
        config_list = list(config.keys())
        config["curr_time"] = curr_time

        if not "run_type" in config:
            raise ValueError("run_type must be defined in config")

        run_type = config["run_type"]
        run_folder = "runs/" + run_type + "_" + str(curr_time) + "/"

        # set current run
        os.environ["CURR_RUN"] = run_folder
        # TODO how about other sensors???
        current_mw_components = ["sut", "attack", "benign", "rtt"]
        mw_run_json: Dict[str, Any] = {}

        # check fields?
        for field in config_list:

            if field in current_mw_components:
                continue

            if field == "run_type":
                continue

            self.logger.warn(f"{field} is an unnecessary field")

        compose_file_string = ""
        compoents = []

        for comp in current_mw_components:

            if comp in config:
                try:

                    current_compoent = mw_prep_compoent(
                        comp, config, mw_run_json, log_level
                    )
                    if current_compoent is not None:
                        compoents.append(current_compoent)
                        # set envs for run
                        status = current_compoent.set_env_variables()

                        if status != 0:
                            raise TypeError("Error setting up environment")
                        # get docker compose string
                        # TODO not sure how to fix mypy error
                        compose_file_string += (
                            "-f " + current_compoent.config["compose-file"] + " "
                        )
                    else:
                        raise TypeError("Invalid compoent")
                except Exception as error:
                    raise TypeError(error)

        mw_run_json["compose_file_string"] = compose_file_string
        return mw_run_json, compoents

    def start_docker_containers(
        self, run_json: Dict[str, Any], config: Dict[str, Any], run_count: int
    ) -> int:
        """
        Purpose:
            Start the docker compose script
        Args:
            run_json: The run parameters json config
            config: The basic run config
            run_count: Current run number
        Returns:
            status: -1 if fail, 0 if pass
        """
        # print("Start docker compose using" + str(config))
        # start docker compose
        run_type = config["run_type"]
        curr_time = config["curr_time"]
        if "sut" in run_json:
            run_duration = run_json["sut"]["run_duration"]
        else:
            self.logger.error("No SUT")
            raise TypeError("No SUT in config")
        compose_file_string = run_json["compose_file_string"]

        signal.signal(signal.SIGINT, partial(signal_handler, run_json))  # type: ignore

        run_loc = (
            "magicwand_components/suts/runs/" + run_type + "_" + str(curr_time) + "/"
        )

        # Create dirs to prevent docker from making them with root permissions
        if not os.path.exists(run_loc):
            os.makedirs(run_loc)

        self.logger.info("Running for " + str(run_duration) + " seconds")
        cmd = "docker-compose " + compose_file_string + " up -d"
        status = os.system(cmd)

        if status != 0:
            self.logger.error("Run " + str(run_count) + " Failed")
            raise OSError("docker-compose failed")

        run_json["run_loc"] = run_loc
        # get magicwand version
        version = Config.VERSION
        run_json["version"] = version
        # dump run options json
        outfilename = run_loc + "run_parms.json"
        try:
            with open(outfilename, "w") as outfile:
                json.dump(run_json, outfile)
        except Exception as error:
            self.logger.error("Run " + str(run_count) + " Failed")
            raise OSError(error)

        outfilename = run_loc + "run_config.json"

        try:
            with open(outfilename, "w") as outfile:
                json.dump(config, outfile)
        except Exception as error:
            self.logger.error("Run " + str(run_count) + " Failed")
            raise OSError(error)

        self.start_non_docker_sensors(run_json)

        return 0

    def start_non_docker_sensors(self, run_json: Dict[str, Any]) -> int:
        """
        Purpose:
            Start non docker sensors
        Args:
            run_json: The run parameters json config
        Returns:
            status: -1 if fail, 0 if pass
        """
        self.logger.debug("starting non docker sensors")
        run_loc = run_json["run_loc"]
        run_duration = run_json["sut"]["run_duration"]
        # TODO what are other non docker sensors we could add?
        return mem_stats(run_loc, run_duration)

    def stop_docker_containers(
        self, run_json: Dict[str, Any], run_count: int, data_version: str
    ) -> int:
        """
        Purpose:
            Stop the docker compose
        Args:
            run_json: The run parameters json config
            run_count: Current run
            data_version: Where data is saved
        Returns:
            status: -1 if fail, 0 if pass
        """
        self.logger.debug("stopping docker")

        run_loc = run_json["run_loc"]
        compose_file_string = run_json["compose_file_string"]
        cmd = "docker-compose " + compose_file_string + " down"
        status = os.system(cmd)

        if status != 0:
            self.logger.error("Run " + str(run_count) + " Failed")
            raise OSError("docker-compose failed")

        # combine ip_maps to attr_map.csv
        ip_maps = [
            "ip_map_attack.csv",
            "ip_map_client.csv",
            "ip_map_rtt.csv",
            "ip_map_sut.csv",
        ]
        rtt_array = []

        for ip_map in ip_maps:
            if os.path.exists(run_loc + ip_map):
                temp_map = pd.read_csv(run_loc + ip_map)
                rtt_array.append(temp_map)

        if len(rtt_array) != 0:
            attr_map = pd.concat(rtt_array, ignore_index=True)
            attr_map.to_csv(run_loc + "ip_attr_map.csv")
        else:
            self.logger.error("No IPs found")
            self.logger.error("Run " + str(run_count) + " Failed")
            return -1

        if os.path.exists(run_loc + "tcpdump.pcap"):
            # run the CIC Converter image
            # docker run --rm -it -v $(PWD):/home CIC_CONVERTER_DOCKER_IMAGE
            # need to use an absolute path for the volume mount
            cmd = f"docker run --rm -v {os.getcwd()}/{run_loc}:/home {CIC_CONVERTER_DOCKER_IMAGE}"
            status = os.system(cmd)

            if status != 0:
                self.logger.error("CIC parse failed")
                return -1

            try:
                cic_data = pd.read_csv(run_loc + "tcpdump.pcap_Flow.csv")
                # for each row label the dataset
                cic_data["Label"] = cic_data.apply(
                    lambda row: label_cic(row, attr_map), axis=1
                )
                print_flow_split(cic_data, self.logger)
                cic_data.to_csv(run_loc + "cic_flow_labeled.csv")
            except Exception as error:
                self.logger.error(error)
                return -1

        try:
            shutil.move(run_loc, "data_runs/" + data_version + "/")
        except Exception as error:
            self.logger.error("mv command failed")
            self.logger.error("Run " + str(run_count) + " Failed")
            raise OSError(error)

        # place finish run here?
        self.logger.info("Finished Run " + str(run_count) + " Successfully")
        return 0

    def post_run_actions(
        self, run_json: Dict[str, Any], data_version: str
    ) -> Dict[str, Any]:
        """
        Purpose:
            Gather data for verfications
        Args:
            run_json: Run config json
            data_version: Current folder for run
        Returns:
            post_run_data: Dictionary with all post run data
        """
        run_prefix = "magicwand_components/suts/runs/"

        run_dir = run_json["run_loc"].replace(run_prefix, "")
        run_loc = "data_runs/" + data_version + "/" + run_dir

        if os.path.exists(run_loc + "tcpdump.pcap"):
            status = run_tshark(run_loc)

            if status != 0:
                self.logger.warn("tshark warning")
                # raise OSError("Tshark failed")

        else:
            raise OSError("No PCAP found")

        try:
            tcpcsv = pd.read_csv(run_loc + "tcpdump_verify.csv", error_bad_lines=False)
        except Exception as error:
            raise OSError(error)

        post_run_data = {}
        post_run_data["tcpcsv"] = tcpcsv
        post_run_data["run_loc"] = run_loc

        if os.path.exists(run_loc + "ip_attr_map.csv"):
            try:
                ip_map = pd.read_csv(run_loc + "ip_attr_map.csv")
                post_run_data["ip_map"] = ip_map
            except:
                raise OSError("Could not open ip_attr_map.csv")

        if "attack" in run_json:

            if os.path.exists(run_loc + "ip_map_attack.csv"):
                try:
                    ip_map_attack = pd.read_csv(run_loc + "ip_map_attack.csv")
                    post_run_data["attack_ips"] = ip_map_attack
                except:
                    raise OSError("Couldnt open ip_map_attack.csv")

        if "benign" in run_json:

            if os.path.exists(run_loc + "ip_map_client.csv"):
                try:
                    ip_map_client = pd.read_csv(run_loc + "ip_map_client.csv")
                    post_run_data["benign_ips"] = ip_map_client
                except:
                    raise OSError("Couldnt open ip_map_client.csv")

        return post_run_data

    def post_run_calibrate(
        self,
        run_json: Dict[str, Any],
        data_version: str,
        attack: str,
        calibrate_component: MwComponent,
    ) -> Dict[str, Any]:
        """
        Purpose:
            Gather data for calibrate
        Args:
            run_json: Run config json
            data_version: Current folder for run
            attack: which attack to calibrate
            calibrate_component: mw_component to use
        Returns:
            post_run_data: Dictionary with all post run data
        """
        run_prefix = "magicwand_components/suts/runs/"

        run_dir = run_json["run_loc"].replace(run_prefix, "")
        run_loc = f"data_runs/{data_version}/{run_dir}"

        if attack == "apachekill":
            # gather apachekill data
            return calibrate_component.get_calibrate_data(run_loc)

        else:
            raise TypeError(f"Invalid attack {attack}")
