# Magicwand Images

These are the docker images needed for magicwand
You can build them with ```build_all.sh``` or pull from docker-hub with ```pull_images.sh```

## SUTS

System Under Test (SUT) is our target server that will be receiving traffic from the clients and attacks.

### Apache SUT

This is a clean Ubuntu 18.04 image with Apache/2.2.11
This version of Apache is vulnerable to attacks.

### Clean WP

This image is built from the Apache SUT and installs WordPress 4.7.3

## Clients

These are images that send non attack data to the SUT

### RTT-Tracker

This is our Round Trip Time (RTT) tracker that will send a request every second to the SUT. It has a timeout of 2 seconds.

### Smart-Swarm

This image uses [Locust](https://locust.io/) to simulate normal traffic sent to the SUT. We have a custom profile that simulates a "9-5 workweek" per 5 minutes, and configuration options to change the behavior of http keepalive.

## Attacks

These images are built to implement the DDOS attacks
Please see the [Attacks page](attacks.md#license) for further details.

## CIC

These images are for the using the CIC (Canadian Institute for Cybersecurity) PCAP to csv pipeline

### Converter 

This image converts PCAPs into a csv with 80 statistical network traffic features such as Duration, Number of packets, Number of bytes, Length of packets, etc.
To learn more visit [CICFlowMeter](https://www.unb.ca/cic/research/applications.html#CICFlowMeter)
