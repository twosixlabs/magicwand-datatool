# Configuration

The following explains the fields mean for each Magicwand component JSONs, and how you can customize it for your experiments.


## Experiment 

Each Magicwand experiment is started from a base config in the configs folder. Experiments can have an attack, benign or both components set.

* attack - Attack component to use (optional)
* benign - Benign component to use (optional)
* sut - SUT component to use (required)
* rtt - rtt component to use (required)
* run_type - Name prefix for run folder (required)


### Example Config

```
{
    "attack": "apachekill",
    "benign": "mw_locust",
    "sut": "mw_apache_wp",
    "rtt": "mw_rtt_sensor",
    "run_type": "mw-locust-apachekill"
}
```

## Benign

### `mw_locust.json`

This is our specialized benign locust client

* benign - Name of benign client
    - client_options - Options for client image
        * num_ips - Number of unique IPs to use
        * client_duration - How long image should send traffic
        * locust_duration - How long individual locusts send traffic
        * wait_max - Maximum time to wait before starting a client
        * stagger - Options to stagger clients
            * ON - Will randomly stagger between 0 and WAIT_MAX seconds each client
            * OFF - No stagger, will use default locust settings
        * keepalive - Options to set http keepalive for clients
            * ON - http keepalive is on, this is default behavior 
            * OFF - http keepalive is off
            * RANDOM - http keepalive will randomly be on or off for each client request
        * seed - Unsigned 32 bit int used as a seed for all python random module generations (None if don’t want to set)
        * traffic_behavior -  24 character string of either ABCDEFGH representing traffic intensity per hour on a scale from 1 - 128  (default if don’t want to change)

   * compose-file - The docker compose file for this component

#### Example Config

``` 
{
  "client_options": {
    "stagger": "ON",
    "num_ips": 20,    
    "client_duration": 300,
    "locust_duration": 300,
    "wait_max": 60              
    "keepalive": "ON"          
    "traffic_behavior": "default"
    "seed": "None"
  },
  "benign": "mw_locust",
  "compose-file": "magicwand_components/benign/mw_locust.yml"
}

```

## Attacks

### `apachekill.json`

This is the apachekill attack client

* attack - Name of attack
    - attack_options - Options for attack image
        * ak_num_threads - Number of threads to spawn
        * ak_num_ips - How many IPs to spawn
        * attack_delay - How long to wait before attack starts
        * ak_duration: How long the attack will go on for
   * compose-file - The docker compose file for this component

#### Example Config

``` 
{"attack_options": {"ak_num_threads": 50, "ak_num_ips": 20, "attack_delay": 15, "ak_duration": 300}, "attack": "apachekill", "compose-file": "magicwand_components/attacks/apachekill.yml"}
```

### `sockstress.json`

This is the Sockstress attack client

* attack - Name of attack
    - attack_options - Options for attack image
        * packet_delay: How long to wait before requests (lower is stronger)
        * attack_duration: How long the attack will go on for 
        * attack_delay - How long to wait before attack starts
   * compose-file - The docker compose file for this component

#### Example Config

``` 
{"attack_options": {"packet_delay": 5000, "attack_duration": 300, "attack_delay": 15}, "attack": "sockstress", "compose-file": "magicwand_components/attacks/sockstress.yml"}
```




### `goloris.json`

This is the Goloris attack client

* attack - Name of attack
    - attack_options - Options for attack image
        * worker_count: How many processes to spawn,
        * ramp_up_interval: How quickly processes spawn
        * attack_duration: How long the attack will go on for
        * attack_delay - How long to wait before attack starts
   * compose-file - The docker compose file for this component

#### Example Config

``` 
{"attack_options": {"worker_count": 16, "ramp_up_interval": 1, "attack_delay": 15, "attack_duration": 300}, "attack": "goloris", "compose-file": "magicwand_components/attacks/goloris.yml"}
```


### `sht_rudeadyet.json`

This is the sht_rudeadyet attack client

* attack - Name of attack
    - attack_options - Options for attack image
        * connections_per_sec: How many connections to spawn per second
        * attack_duration: How long the attack will go on for
        * num_connections": Number of connections to make
        * attack_delay - How long to wait before attack starts
   * compose-file - The docker compose file for this component

#### Example Config

``` 
{"attack_options": {"connections_per_sec": 256, "attack_duration": 300, "num_connections": 16384,"attack_delay": 15}, "attack": "sht_rudeadyet", "compose-file": "magicwand_components/attacks/sht_rudeadyet.yml"}
```


### `sht_slowloris.json`

This is the sht_slowloris attack client

* attack - Name of attack
    - attack_options - Options for attack image
        * connections_per_sec: How many connections to spawn per second
        * attack_duration: How long the attack will go on for
        * num_connections": Number of connections to make
        * attack_delay - How long to wait before attack starts
   * compose-file - The docker compose file for this component

#### Example Config

``` 
{"attack_options": {"connections_per_sec": 256, "attack_duration": 300, "num_connections": 16384,"attack_delay": 15}, "attack": "sht_rudeadyet", "compose-file": "magicwand_components/attacks/sht_slowloris.yml"}
```

### `sht_slowread.json`

This is the sht_slowread attack client

* attack - Name of attack
    - attack_options - Options for attack image
        * connections_per_sec: How many connections to spawn per second
        * attack_duration: How long the attack will go on for
        * num_connections": Number of connections to make
        * attack_delay - How long to wait before attack starts
   * compose-file - The docker compose file for this component

#### Example Config

``` 
{"attack_options": {"connections_per_sec": 256, "attack_duration": 300, "num_connections": 16384,"attack_delay": 15}, "attack": "sht_rudeadyet", "compose-file": "magicwand_components/attacks/sht_slowread.yml"}
```



## SUT

### `mw_apache_wp.json`

This is the mw_apache_wp SUT

* sut - Name of SUT
* max_clients - Maximum number of httpd processes that can spawn
* run_duration - How long Magicwand run is
* pcap_snap_length - How many bytes to capture per packet from tcpdump
* compose-file - The docker compose file for this component

#### Example Config

```
{"pcap_snap_length": 400 , "max_clients": 250,  "run_duration": 300, "sut": "mw_apache_wp", "compose-file": "magicwand_components/suts/mw_apache_wp.yml"}
```


## Sensors


### `mw_rtt_sensor.json`

This is the rtt sensor

* rtt - Name of rtt sensor
* compose-file - The docker compose file for this component
* timeout - How many seconds for request to wait before timeout


#### Example Config

```
{"rtt":"mw_rtt_sensor", "compose-file": "magicwand_components/sensors/mw_rtt_sensor.yml", "timeout": 2}
```
