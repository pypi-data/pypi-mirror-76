#!/usr/bin/env bash
#
# A Simple Shell Script to Upload Media Packages and Log Files
#
# John Poncini
# Video and Informatics Systems Associate
# MAPS Public Benefit Corporation
# 17 September 2019

while read d; 
    do data+=($d);
done < "/etc/opt/adam/device.conf"
declare -p data

SSID=${data[1]}
PSK=${data[2]}

wpa_supplicant -B -i wlan0 -c <(wpa_passphrase $SSID $PSK)
