---
title: 'Wifi-Mesh-Evlauation: Bandwith to Distance Relation'
date: '2024-08-08T21:45:17+02:00'
author: 'Giancarlo Rizzo'
draft: false
categories: [analysing]
color: '#a09f93'
---

# Prologue

While working for a new project one task was to transfer data from a moving vehicle to a receiving device behind a wifi-mesh. The two accesspoints of the mesh were placed along the street and the question about the bandwith-capabilities depending on the distance to the nearest accesspoint and the distance to the center of the wifi-mesh became important. 

## Expecations

The goal of this evaluation was to checkout the minimum distance for a suitable connection with acceptable bandwith and latency. Moreover any connectivity-issues during a handover-action between the two accesspoints should be indicated to make sure that this setup could work.

# Setup

```bash
host_a --- connection via wifi --- accesspoint_1 --- lan --- host_b 
                               |-- accesspoint_2 --|
```

## Setup host_b

To measure the bandwith between these two hosts (host_a and host_b) I've setup an iperf3-server running as deamon on the stationary _host_b which is listening by default on port 5201.

```bash
# on stationary host_b
sudo iperf3 -s -D
```

## Setup host_a

On the vehicle-device I needed to setup quite a few things.

- iperf3-client and permanent logging of current bandwith
- logging of the gps-position of the vehicle
- loggin  of the latency via icmp between the vehicle (host_a) and the stationary-target (host_b) 

The hardware was stored in the trunk and the external antennas for the gps-logging and wifi-connection were mounted on the roof.

To log the gps-data via the usb-gps-antenna I had to set up a gpsd-socket listening to a usb-gps-antenna within a screen:

```bash
# stop gpsd to listen run it with sudo-privileges and listening on serial-input
sudo systemctl stop gpsd.service
sudo systemctl stop gpsd.socket

# open screen
screen -S gps
# whitin the screen run gpsd-socket and listen to usb-gps-antenna
sudo gpsd -n -N 5 /dev/ttyACM0 
# ...

# deattach screen afterwards with ctrl+A+D
```

After the gps-socket was running and communicating through the serial-interface, I started a script that runs the three logging-tasks from above and kills the latency-measurement and gps-measurement until the iperf3-client finished its bandwith-tests.

Here is this the measurement.sh which I started via `sudo ./measurement.sh`:

```bash
#!/bin/bash

measurement_time=60
host_b="192.168.2.1"

# start gps-measurement
echo "Start Position-Tracking:"
gpspipe -w > "gpsdata_$(date +%d%m%Y_%H_%M_%S.log)" &

# start latency-measurement
echo "Start latency-measurement"
ping $host_b >>  "icmp_$(date +%d%m%Y_%H_%M_%S).log" &

# start bandwith-measuement
echo "Start bandwith-measuement via iperf3 for $measurement_time seconds."
sudo iperf3 -c $host_b -i 1 -t $measurement_time --logfile  "_bandwith$(date +%d%m%Y_%H_%M_%S).log"

#stop measurements after bandwith-measurement is finished
killall ping
killall gpspipe
```

This little script creates three log-files which are containing the starttime-information in their filename. 

This starttime is important for the data-syncing in the next postprocessing to find the correct relation between the gps-position and the latency-measurement and bandwith-measurement.

# Postprocessing

The implementation of postprocessing is about three tasks:

- parsing the logs
- syncing the parsed data
- calculate distance according to each datapoint

To run the postprocessing-script execute:

```bash
# for first info
pipenv run python ./evaluation/__main__.py --help

# to process all data from ONE accesspoint
pipenv run python ./evaluation/__main__.py -b -g -i -s ./data/<measurementfolder>/

# to process all data from two accesspoints add -m 
pipenv run python ./evaluation/__main__.py -b -g -i -s -m ./data/<measurementfolder>/
```

The results are seved into a `result/<measurementfolder>/<time>.csv`-file.

# Evaluation

For the evaluation of the measurements I created a Jupyter-Notebook for each the single-accesspoint-measurements and a second one for each of the two-accesspoint-measurements (mesh).

_To ckeck out about the evaluation in detail take a look at the following notebooks:_

- _[single-ap-evaluation](https://github.com/protogia/WIFI-Mesh-Evaluation/blob/main/evaluation/evaluate_single_AP_connection.ipynb)_
- _[mesh-evaluation](https://github.com/protogia/WIFI-Mesh-Evaluation/blob/main/evaluation/evaluate_dual_mesh_wlan_connection.ipynb)_
