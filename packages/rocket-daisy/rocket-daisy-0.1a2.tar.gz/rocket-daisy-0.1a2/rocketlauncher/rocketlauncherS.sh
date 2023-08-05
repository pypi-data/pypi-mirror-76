#!/bin/bash

# Project skidloader
# This is the script required for autostarting
# all dependent executables
# and is getting called by rocket.services launcher
# at the boot time

# Author: Martin Shishkov
# Created : 05.03.2020
#

echo "gulliversoft, starting capture loop"
# tail -F /var/log/syslog | grep --line-buffered 'IEEE 802.11: associated'|
# { read line;
# echo $line;
 ln -s /dev/ttyUSB0 /dev/serial0;
 sudo $PWD/RIB_App & 
 daisy -c /etc/daisy/config &
 sudo $PWD/Digger_Consumer_App;
# exit 0; } 
