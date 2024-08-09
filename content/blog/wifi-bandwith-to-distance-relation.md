---
title: 'Wifi Bandwith to Distance Relation'
date: '2024-08-08T21:45:17+02:00'
author: 'Giancarlo Rizzo'
draft: true
categories: []
color: '#ffcc66'
titleimage: 'content/blog/titleimages/CHANGEME.png'
---

# Prologue

While working for a new project one task was to transfer data from a moving vehicle to a receiving device behind a wifi-mesh. The two accesspoints of the mesh were placed along the street and the question about the bandwith-capabilities depending on the distance to the nearest accesspoint and the distance to the center of the wifi-mesh became important. 

```
host_a --- connection via wifi --- accesspoint_1 --- lan --- host_b 
                               |-- accesspoint_2 --|
```

## Setup

To measure the bandwith between these two hosts (host_a and host_b) I've setup an iperf3-server running as deamon on the stationary _host_b which is listening by default on port 5201.

```bash
# on stationary host_b
sudo iperf3 -s -D
```

On the vehicle-device I needed to setup quite a few things.

- iperf3-client and permanent logging of current bandwith
- logging of the gps-position of the vehicle
- loggin  of the latency via icmp between the vehicle (host_a) and the stationary-target (host_b) 

For this purpose just setup a gpsd-socket listening to a usb-gps-antenna within a screen:

```bash
# stop gpsd to listen run it with sudo-privileges and listening on serial-input
sudo systemctl stop gpsd.service
sudo systemctl stop gpsd.socket

# open screen
screen -S gps
# whitin the screen run gpsd-socket and listen to usb-gps-antenna
sudo gpsd -n -N 5 /dev/ttyACM0 
# ...

# deatach screen with ctrl+A+D
```

Now that gps is running through the serial-interface I started a script that runs the three logging-tasks from above and kills the latency-measurement and gps-measurement after the iperf3-client is finishing its bandwith tests.

Here is this the measurement.sh which I started via `sudo ./measurement.sh`:

```bash
#!/bin/bash
# ...
```
