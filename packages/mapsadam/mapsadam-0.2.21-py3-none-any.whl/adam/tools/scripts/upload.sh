#!/usr/bin/env bash
#
# A Simple Shell Script to Upload Media Packages and Log Files
#
# John Poncini
# Video and Informatics Systems Associate
# MAPS Public Benefit Corporation

declare -A TYPE
declare -A BUCKET

TYPE=( \
    ["key"]="keys" \
    ["gz"]="packages" \
)
BUCKET=( \
    ["MP18"]="maps-eu-videos" \
    ["MAPP3"]="maps-study-videos" \
    ["MAPP1"]="maps-study-videos" \
)
LOGPATH="s3://maps-eu-videos/ingest/logs/"$(date +%Y%m%d-%H%M%S)"/"

for FILENAME in $(ls /var/local/pkg/); do

    STUDY=$(echo $FILENAME | cut -d"_" -f1)
    FILETYPE=$(echo $FILENAME | rev | cut -d"." -f2 | rev)
    FILEPATH=$(echo $FILENAME | tr "_" "/")
    S3PATH="s3://${BUCKET[${STUDY}]}/ingest/${TYPE[${FILETYPE}]}/${FILEPATH}"

    s4cmd put /var/local/pkg/${FILENAME} \
        $S3PATH \
        --multipart-split-size=16777216 \
        --max-singlepart-upload-size=16777216 \
        --API-Metadata=$(cat /tmp/metadata.json) \
    && rm /var/local/pkg/${FILENAME}
cat
done;

for LOGFILE in $(ls /tmp/*.log); do

    s4cmd put ${LOGFILE} \
        ${LOGPATH}$(echo $LOGFILE | cut -f3 -d"/") \
        --multipart-split-size=16777216 \
        --max-singlepart-upload-size=16777216 \

done;
