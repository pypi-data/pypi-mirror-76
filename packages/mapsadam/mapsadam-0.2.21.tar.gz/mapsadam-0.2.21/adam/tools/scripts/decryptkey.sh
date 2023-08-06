#!/usr/bin/env bash
#
# A Simple Shell Script to Decrypt USB Keys
#
# John Poncini
# Video and Informatics Systems Associate
# MAPS Public Benefit Corporation
# 17 September 2019
sudo openssl rsautl -decrypt -inkey /etc/keys/usb/private.key \
   -in /mnt/key/bin.enc -out /tmp/usb.key
