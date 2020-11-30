## Data

Each Magicwand experiment will generate data that can be used for modeling purposes to identify attack and client traffic.
This document will go over how each of these files is generated. How you use them is up to you

```
apache_stats.csv        ip_map_client.csv       mem_stats.csv           tcpdump.pcap
cic_flow_labeled.csv    ip_map_rtt.csv          rtt_stats.csv           tcpdump.pcap_Flow.csv
ip_attr_map.csv         ip_map_sut.csv          run_config.json         tcpdump_verify.csv
ip_map_attack.csv       locust_4ce7ab68e5df.csv run_parms.json          verify_run.json   
```

### tcpdump.pcap

This is the PCAP generated for each experiment. PCAPs hold the raw network traffic data and are the basis for most network security datasets.

This is the command used to collect the PCAP for each experiment.
```
tcpdump -vvv -i any -s $PCAP_SNAP_LEN -w /home/tcpdump.pcap
```

### tcpdump_verify.csv


To verify the data for each experiment, we used tshark to convert the raw PCAP into a CSV. With this CSV we can do some data validation steps to ensure that the data is correct. This is the tshark command run automatically post-experiment to convert the PCAP to a CSV.

```
tshark -r tcpdump.pcap -i wlan1 -T fields -E header=y -E separator=, -E quote=d -e _ws.col.No. -e _ws.col.Time -e _ws.col.Source -e _ws.col.Destination -e _ws.col.Protocol -e _ws.col.Length -e _ws.col.Info  -e http.user_agent -e http.connection -e http.request -e http.request.line > tcpdump_verify.csv
```
To learn more about how you can use tshark to convert the PCAP for your needs [click here](https://tshark.dev/)  



This is a glimpse of what the tcpdump_verify.csv file looks like.
```
_ws.col.No.,_ws.col.Time,_ws.col.Source,_ws.col.Destination,_ws.col.Protocol,_ws.col.Length,_ws.col.Info,http.user_agent,http.connection,http.request,http.request.line
"1","0.000000","192.168.32.4","192.168.32.2","TCP","74","39684 → 80 [SYN] Seq=0 Win=1152 Len=0 MSS=1460 SACK_PERM=1 TSval=1823557209 TSecr=0 WS=1",,,,
"2","0.001309","192.168.32.4","192.168.32.2","TCP","74","39246 → 80 [SYN] Seq=0 Win=1152 Len=0 MSS=1460 SACK_PERM=1 TSval=1823557211 TSecr=0 WS=1",,,,
"3","0.001316","192.168.32.4","192.168.32.2","TCP","74","39244 → 80 [SYN] Seq=0 Win=1152 Len=0 MSS=1460 SACK_PERM=1 TSval=1823557211 TSecr=0 WS=1",,,,
```


### verify_run.json

This JSON file depicts the output of the experiment verifier.    
Each component has its own verify function and will return true or false if the experiment checks passed.

```
{
  "MW_Apache_WP": true,
  "Apachekill": true,
  "MW_Locust": true,
  "MW_RTT_Sensor": true,
  "MW_Global": true
}
```


### rtt_stats.csv

This is a CSV file produced by the Round-Trip Time (RTT) tracker that collects how long each request took. This file can be used to measure how responsive the SUT was during each experiment.

* timestamp - Seconds since experiment started
* rtt - Round Trip time in seconds for a request to be sent

```
timestamp,rtt
0,0.007287
1,0.002221
2,0.003041
3,0.001833
4,0.002691
```

### ip_attr_map.csv

This is an IP attribution csv that keeps track of what each IP is i.e. is it an attack or benign client. This file is an aggregate of the following files

```
ip_map_sut.csv ip_map_attack.csv ip_map_client.csv ip_map_rtt.csv
```

The following explains what each field means.  

* index - Number in csv
* ip - IP address in the experiment
* type - Type of traffic attack, client or from the SUT
* subtype - More granular view of IP such as attack name 

```
index,ip,type,subtype
0,192.168.1.1,attack,apachekill
1,192.168.1.2,attack,apachekill
2,192.168.1.3,attack,apachekill
3,192.168.1.4,attack,apachekill
4,192.168.1.5,attack,apachekill
5,192.168.2.1,attack,apachekill
6,192.168.2.2,attack,apachekill
7,192.168.2.3,attack,apachekill
8,192.168.2.4,attack,apachekill
```


### locust_HOSTNAME.csv

This is csv is produced by locust. It catalogs the requests and fails at each timestamp
The following explains what each field means.  


* timestamp -local time for image
* requests - Number of successful connections
* fails - Number of failed connections

```
timestamp,requests,fails
14:47:33,0,0
14:47:34,0.0,0
14:47:35,0.0,0
14:47:36,0.0,0
14:47:37,2.0,0
14:47:38,2.6666666666666665,0
```

### apache_stats.csv 

This csv is produced by apache. it catalogs various system metrics during the run.
The following explains what each field means.  


* timestamp - Seconds since experiment started
* total_access - Total number of requests 
* total_traffic - Size of traffic transferred to clients 
* cpu_load - CPU usage of Apache image
* requests per second - Number of requests per second
* httpd mem used(kb) - Memory used from httpd processes
* num_httpd - Number of httpd processes spawned
* system memory free - Total system memory free

```
timestamp,total_access,total_traffic,cpu_load,requests per second,httpd mem used(kb),num_httpd,system memory free
1.0,94,369 kB,.2%,18.8,22728,9,3499
2.0,99,375 kB,.167%,16.5,28528,11,3498
3.0,105,382 kB,.286%,15,40088,15,3497
4.0,112,389 kB,.375%,14,63168,23,3495
5.0,120,398 kB,.333%,13.3,63112,23,3494
6.0,129,407 kB,.3%,12.9,63140,23,3494
7.0,139,418 kB,.273%,12.6,63112,23,3493
9.0,150,430 kB,.25%,12.5,66116,25,3492
10.0,162,442 kB,.231%,12.5,72000,26,3492

```

### mem_stats.csv

This csv shows system memory being used by the SUT as reported from docker stats.
The following explains what each field means.  

* timestamp - Seconds since experiment started
* memory_percent - Memory usage reported by docker stats

```
timestamp,memory_percent
3,2.21
10,2.36
17,7.12
25,15.24
32,17.63
40,25.41
48,27.44
55,29.6
63,34.9
```

### run_config.json

This is the run config used to start the experiment.  
For details on the component fields view the [configuration page](config.md#) for details on what each field means.  
```
{
    "attack": "apachekill",
    "benign": "mw_locust",
    "sut": "mw_apache_wp",
    "rtt": "mw_rtt_sensor",
    "run_type": "mw-locust-apachekill"
}
```


### run_params.json

This is the JSON file that was used to configure the experiment.   

These are the run metadata fields.  
* "compose_file_string": docker compose file string
* "run_loc": Location of run data
* "version": Version of magicwand used to generate data


For details on the component fields view the [configuration page](config.md#) for details on what each field means.


```
{
  "sut": {
    "pcap_snap_length": 400,
    "max_clients": 250,
    "run_duration": 300,
    "sut": "mw_apache_wp",
    "compose-file": "magicwand_components/suts/mw_apache_wp.yml"
  },
  "attack": {
    "attack_options": {
      "ak_num_threads": 50,
      "ak_num_ips": 20,
      "attack_delay": 15,
      "ak_duration": 300
    },
    "attack": "apachekill",
    "compose-file": "magicwand_components/attacks/apachekill.yml"
  },
  "benign": {
    "client_options": {
      "stagger": "ON",
      "num_ips": 20,
      "client_duration": 300,
      "locust_duration": 300,
      "wait_max": 10,
      "keepalive": "ON",
      "traffic_behavior": "HHHHHHHHHHHHHHHHHHHHHHHH"
    },
    "benign": "mw_locust",
    "compose-file": "magicwand_components/benign/mw_locust.yml"
  },
  "rtt": {
    "rtt": "mw_rtt_sensor",
    "compose-file": "magicwand_components/sensors/mw_rtt_sensor.yml",
    "timeout": 2
  },
  "compose_file_string": "-f magicwand_components/suts/mw_apache_wp.yml -f magicwand_components/attacks/apachekill.yml -f magicwand_components/benign/mw_locust.yml -f magicwand_components/sensors/mw_rtt_sensor.yml ",
  "run_loc": "magicwand_components/suts/runs/mw-locust-apachekill_10_29_2020T10_37_57Z/",
  "version": "beta-1.0.0"
}
```


### cic_flow_labeled.csv

This is a labeled csv has 80 statistical network traffic features such as Duration, Number of packets, Number of bytes, and Length of packets for each bidirectional flow in the PCAP. 

The labels are `attack` for attack clients and `client` for benign clients.

!!! note 
    tcpdump.pcap_Flow.csv is the unlabeled version of the csv

To learn more about the features visit [here](https://github.com/CanadianInstituteForCybersecurity/CICFlowMeter/blob/master/ReadMe.txt#L80)

Here is an example output
```
,Flow ID,Src IP,Src Port,Dst IP,Dst Port,Protocol,Timestamp,Flow Duration,Total Fwd Packet,Total Bwd packets,Total Length of Fwd Packet,Total Length of Bwd Packet,Fwd Packet Length Max,Fwd Packet Length Min,Fwd Packet Length Mean,Fwd Packet Length Std,Bwd Packet Length Max,Bwd Packet Length Min,Bwd Packet Length Mean,Bwd Packet Length Std,Flow Bytes/s,Flow Packets/s,Flow IAT Mean,Flow IAT Std,Flow IAT Max,Flow IAT Min,Fwd IAT Total,Fwd IAT Mean,Fwd IAT Std,Fwd IAT Max,Fwd IAT Min,Bwd IAT Total,Bwd IAT Mean,Bwd IAT Std,Bwd IAT Max,Bwd IAT Min,Fwd PSH Flags,Bwd PSH Flags,Fwd URG Flags,Bwd URG Flags,Fwd Header Length,Bwd Header Length,Fwd Packets/s,Bwd Packets/s,Packet Length Min,Packet Length Max,Packet Length Mean,Packet Length Std,Packet Length Variance,FIN Flag Count,SYN Flag Count,RST Flag Count,PSH Flag Count,ACK Flag Count,URG Flag Count,CWR Flag Count,ECE Flag Count,Down/Up Ratio,Average Packet Size,Fwd Segment Size Avg,Bwd Segment Size Avg,Fwd Bytes/Bulk Avg,Fwd Packet/Bulk Avg,Fwd Bulk Rate Avg,Bwd Bytes/Bulk Avg,Bwd Packet/Bulk Avg,Bwd Bulk Rate Avg,Subflow Fwd Packets,Subflow Fwd Bytes,Subflow Bwd Packets,Subflow Bwd Bytes,FWD Init Win Bytes,Bwd Init Win Bytes,Fwd Act Data Pkts,Fwd Seg Size Min,Active Mean,Active Std,Active Max,Active Min,Idle Mean,Idle Std,Idle Max,Idle Min,Label
0,172.18.0.4-172.18.0.2-37402-80-6,172.18.0.4,37402,172.18.0.2,80,6,18/09/2020 02:58:46 PM,1151,5,3,146.0,334.0,146.0,0.0,29.2,65.29318494299386,334.0,0.0,111.33333333333331,192.83498990933498,417028.6707211121,6950.4778453518675,164.42857142857144,269.1758143808969,748.0,12.0,1151.0,287.75,327.5956603294169,748.0,41.0,337.0,168.5,99.7020561473032,239.0,98.0,0,0,0,0,168,104,4344.0486533449175,2606.429192006951,0.0,334.0,53.33333333333334,115.7972365818805,13409.0,1,2,0,2,7,0,0,0,0.0,60.0,29.2,111.33333333333331,0,0,0,0,0,0,0,18,0,41,29200,235,1,32,0.0,0.0,0.0,0.0,1600441126433346.0,0.0,1600441126433346.0,1600441126433346.0,client
```
