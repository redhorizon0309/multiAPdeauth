#!/bin/bash
echo "$#"
if [[ $# -gt 1 ]]; then
    echo "Usage: bash monitor-mode-down.sh [interface]"
elif [[ $# -eq 1 ]]; then
    interface = "$1"
elif [[ $# -eq 0 ]]; then
    interface = "wlan0"
fi
echo $interface
sudo ifconfig $interface down
sudo iwconfig $interface mode monitor
sudo ifconfig $interface up
