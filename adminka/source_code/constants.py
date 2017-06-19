#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#pylint: skip-file
import os

CHANNEL = 6
PUBLIC_DNS = "8.8.8.8"
NETWORK_IP = "192.168.74.0"
NETWORK_MASK = "255.255.255.0"
NETWORK_GW_IP = "192.168.74.1"

DHCP_LEASE = "192.168.74.2,192.168.74.100,12h"

WIFI_BROADCAST = "ff:ff:ff:ff:ff:ff"
WIFI_INVALID = "00:00:00:00:00:00"

LINES_OUTPUT = 3
DN = open('log_output.txt', 'w')
ER = open('log_error.txt', 'w')
