#!/usr/bin/env bash
#
# A Simple Shell Script to Package and Encrypt Media Files
#
# John Poncini
# Video and Informatics Systems Associate
# MAPS Public Benefit Corporation
# 17 September 2019

while read d;
    do data+=($d);
done < "/etc/opt/adam/default.info"
declare -p data

FILEPATH="/var/local/media/${data[0]}_${data[2]}_${data[3]}"
FILENAME="${data[0]}_${data[2]}_${data[3]}_"$(date +%Y%m%d-%H%M%S)
STUDY="${data[0]}"

if [ $STUDY == "MT1" ] || [ $STUDY == "MT2" ]; then
    sudo mount /dev/sda1 /media/usb -o uid=pi,gid=pi
    sudo cp ${FILEPATH} /media/usb/

else
    openssl rand 128 > /tmp/${FILENAME}.key

    openssl rsautl -encrypt -inkey /etc/keys/public.pem -pubin \
        -in /tmp/${FILENAME}.key -out /var/local/pkg/${FILENAME}.key.enc

    tar -czv ${FILEPATH} | openssl aes-256-cbc -out \
        /var/local/pkg/${FILENAME}.tar.gz.enc -pass file:"/tmp/${FILENAME}.key"

    rm /tmp/${FILENAME}.key
    rm -R $FILEPATH

    bash -c "sudo supervisorctl start upload"

fi;
