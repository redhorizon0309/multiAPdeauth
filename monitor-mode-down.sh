#!/bin/bash
if [[ $# -gt 1 ]]; then
    echo "Usage: bash monitor-mode-down.sh [interface]"
elif [[ $# -eq 1 ]]; then
    interface = $1
elif [[ $# -eq 0 ]]; then
    interface = "wlan0"
fi
sudo ifconfig $interface down
sudo iwconfig $interface mode managed
sudo ifconfig $interface up

