# Attacks

Magicwand uses "low volume" DDOS attacks in the data generation runs. The following are all the attacks included in the tool. 

## Apachekill

The ApacheKill attack abuses the HTTP protocol by requesting that the target web server return the requested URL content in a huge number of individual chunks, or byte ranges. It uses up a significant amount of memory on the target web server.

More info: <https://github.com/tkisason/KillApachePy>


## Sockstress

Sockstress is a Denial of Service attack on TCP services, it works by using RAW sockets to establish many TCP connections to a listening service. Because the connections are established using RAW sockets, connections are established without having to save any per-connection state on the attacker's machine.

Like SYN flooding, Sockstress is an asymmetric resource consumption attack: It requires very little resources (time, memory, and bandwidth) to run a Sockstress attack, but uses a lot of resources on the victim's machine. Because of this asymmetry, a weak attacker (e.g. one bot behind a cable modem) can bring down a rather large web server.

More info: <https://github.com/defuse/sockstress>

 
## Goloris

Goloris works by occupying and keeping many TCP connections open to the victim. It uses low network bandwidth to prolong the attack. The goal is to eventually consume all available connections to the victim, so no other client could connect to it.

More info: https://github.com/valyala/goloris

## SlowHTTPTest

SlowHTTPTest is a highly configurable tool that simulates some Application Layer Denial of Service attacks by prolonging HTTP connections in different ways.

It implements most common low-bandwidth Application Layer DoS attacks, such as Slowloris, Slow HTTP POST, Slow Read attack (based on TCP persist timer exploit) by draining concurrent connections pool, as well as Apache Range Header attack by causing very significant memory and CPU usage on the server.

Slowloris and Slow HTTP POST DoS attacks rely on the fact that the HTTP protocol, by design, requires requests to be completely received by the server before they are processed. If an HTTP request is not complete, or if the transfer rate is very low, the server keeps its resources busy waiting for the rest of the data. If the server keeps too many resources busy, this creates a denial of service. This tool is sending partial HTTP requests, trying to get denial of service from target HTTP server.

More info: <https://tools.kali.org/stress-testing/slowhttptest>
