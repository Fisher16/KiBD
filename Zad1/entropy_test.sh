#!/bin/bash

size=$1
start_S=$(cat /proc/sys/kernel/random/entropy_avail)
echo "Reading $size"
sleep_val=$2
for i in `seq 10`
do
    head -c $size /dev/random > /dev/null
    sleep $sleep_val
done

stop_S=$(cat /proc/sys/kernel/random/entropy_avail)
delta=$(($stop_S-$start_S))
echo "Delta entropy $(echo $delta/(10*$sleep_val) | bc)"
