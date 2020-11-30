# CSL Magicwand User Guide

**This guide will explain how to generate datasets for CSL**

## What is Magicwand 
Magicwand is a platform to provide high-quality, reliable, and reproducible data sets for low-and-slow DDoS attacks. With the use of Docker images and customizable JSON files, users can generate a multitude of network traffic PCAPS, that are converted to CSVs labeled with attack or benign network flows.

## Installing Magicwand

For full details checkout the official [README.md](../README.md#installing-magicwand) file in the root of the repository.

### Quick install
```
git clone https://github.com/twosixlabs/magicwand-datatool
cd images
./build_all.sh
cd ..
cd magicwand-data-generator
pip install --editable .
```

### Create CSL datasets

Here's how you can begin creating CSL datasets


**1. Create Dataset Folder**  

This step initializes a magicwand 'environment' to begin running your experiments 

```bash
localhost$ magicwand init --project csl_datasets
localhost$ cd csl_datasets
```

**2. Start an experiment**  

Once your environment is initialized, you can begin creating data using the run command


localhost$ magicwand run --config configs/mw-locust-apachekill.json --count 1 –data_version test_runs


The run config file specifies what components to use for your experiment  
Here is an example of a run config file

```
{
    "attack": "apachekill",
    "benign": "mw_locust",
    "sut": "mw_apache_wp",
    "rtt": "mw_rtt_sensor",
    "run_type": "mw-locust-apachekill"
}
```

The count parameter specifies how many times to run the experiment  
The data_version parameter specifies where to save the data



**3. Evaluate data**  

Each run will output metrics of the final CSV benign vs attack split for the cic_flow_labeled.csv

```
2020-10-21 13:44:29,005 - INFO -  mw-log - Benign Stats:
2020-10-21 13:44:29,005 - INFO -  mw-log - 744 flows out of 1750 flows: 0.43
2020-10-21 13:44:29,005 - INFO -  mw-log - Attack Stats:
2020-10-21 13:44:29,005 - INFO -  mw-log - 1005 flows out of 1750 flows: 0.57
```

If the resulting CSV does not have the desired stats, then we need to edit the component config 

**4. Edit Config files**  

### Editing Attack Configs
Each component config has its own set of parameters to configure in order to affect the number of flows in each experiment.

All components configs are located in the magicwand_components folder.
In this example we will edit the Apachekill Config located here `magicwand_components/attacks/apachekill.json`

``` bash
cat magicwand_components/attacks/apachekill.json | jq
{
  "attack_options": {
    "ak_num_threads": 50,              <- Play around with
    "ak_num_ips": 20,                  <- Play around with
    "attack_delay": 15,                <- Play around with
    "ak_duration": 30                  <- Play around with.  (My experience so far time is biggest factor)
  },
  "attack": "apachekill",
  "compose-file": "magicwand_components/attacks/apachekill.yml"
}

```

ak_num_threads -> How many apachekill threads to start, effect how strong the attack is  
ak_num_ips -> How many unique IPS to use  
attack_delay -> How long to wait before attack starts  
ak_duration -> How long the attack runs for  

The goal of tuning this config is to find out which of these parameters can result in a more even split of data. My experience so far is how long the attack runs determine how many attack flows get generated.

**Note** Since apachekill is a memory consumption attack a high value of ak_num_threads (>100) can fully utilize the RAM on weaker systems.


### Editing Benign Configs

In this example we will edit the MW_Locust Config located here `magicwand_components/benign/mw_locust.json `


```bash
{
  "client_options": {
    "stagger": "ON",                     <- Play around with
    "num_ips": 20,                       <- Play around with (My experience so far num_ips is biggest factor)
    "client_duration": 300,              <- Play around with
    "locust_duration": 300,              <- Play around with
    "wait_max": 60                       <- Play around with
    "keepalive": "ON"                    <- Play around with
    "traffic_behavior": "default"        <- See Traffic behavior section below

  },
  "benign": "mw_locust",
  "compose-file": "magicwand_components/benign/mw_locust.yml"
}

```

stagger -> Determines if clients should randomly start up or start all at once. Can either be "ON" or "OFF"  
num_ips -> Determines how many unique IPs to use  
client_duration -> How long each client is sending connections  
locust_duration -> How long the container is up for  
wait_max -> The max wait time of the random start up interval
keepalive -> Requests will send http keepalive flag can be ON,OFF, or RANDOM
traffic_behavior: The traffic pattern the clients will use

Benign clients don’t generate as much flows as attack traffic, so increasing the number of clients has the biggest effect on how many flows are generated.

### Traffic behavior

Our Locust container comes with a "smart profile" that can be configured to give clients a more "realistic" traffic pattern.

The pattern is configurable to act on a simulated "per hour basis" using our time compression algorithm which determines how much delay to have between requests. The algorithm works like this...    

1. Determine where in the behavior pattern our current time is
2. Select the behavior pattern value just before, and just after our current time (bounding pattern)
3. Interpolate the two bounding patterns values into approximate requests per hour
4. Interpolate requests per hour into seconds between requests
5. Linearly interpolate to determine our current seconds between requests
6. Scale seconds between requests by the ratio of seconds_per_hour and 3600

There are 8 possible behavior states for the clients 
 
```bash
"requests_per_hour": {
        "A": 1,
        "B": 2,
        "C": 4,
        "D": 8,
        "E": 16,
        "F": 32,
        "G": 64,
        "H": 128
}
```

#### Example traffic behavior patterns
Here are some example behavior patterns to try. Each client in the experiment will use the same pattern.

* Default Config
The default config is 
`AAAAAAAAAAAAAAAAAAAAAAAA`   

This means that at every "hour" the clients are sending a simulated 1 request per hour.

* Super Max Config
The "strongest" config would be all H for each of the 24 hours  
`HHHHHHHHHHHHHHHHHHHHHHHH`  


This means that at every "hour" the clients are sending a simulated 128 requests per hour.

* Mix and Match

Here is a config that is "sleeping" during off hours, and has lots of activity during "working hours"

`AAAAAAABHDEFGBAAAAAAAA`  

### Editing Experiment Duration

To make experiments longer or shorter, you need to change the run duration of the SUT(System Under Test)   
The config file is located here `magicwand_components/suts/mw_apache_wp.json`


```bash
{
  "pcap_snap_length": 400,
  "max_clients": 250,                              <-  Max number of concurrent clients
  "run_duration": 300,                             <-  Run duration 
  "sut": "mw_apache_wp",
  "compose-file": "magicwand_components/suts/mw_apache_wp.yml"
}
```

Once the SUT stops, all other containers will also shutdown

### Editing Component Resource Usage

If we wanted to limit how much resources a component uses, you can edit the component docker.yml file  

For example, we can edit the SUT be editing this file `magicwand_components/suts/mw_apache_wp.yml`

```
version: '2.2'
services:

  mw-sut-apachewp:
    image: mw-sut-apachewp:latest
    privileged: true
    ports:
      - "80:80"
    environment:
      - TEST_DURATION=${CURR_TEST_DURATION}
      - MAX_CLIENTS=${CURR_MAX_CLIENTS}
      - PCAP_PACKET_SNAPLEN=${CURR_PCAP_PACKET_SNAPLEN}
    volumes:
      - ./${CURR_RUN}:/home/
    #mem_limit: 16G     <- Uncomment and set how much memory to use
    #cpus: 8  <- Uncomment and set how many CPUs to use
```

### Editing Advice

While there are lots of editable features, for the purposes of a CSL dataset, Attack duration, Attack Strength, number of clients IPS, and client duration seem to have the biggest effect on how many flows are generated. Each Attack will have a sweet spot to play around with.

**5. Repeat Runs**  
Once everything is configured you can do another run, to see if you get the results you desired. if Not back to step 4