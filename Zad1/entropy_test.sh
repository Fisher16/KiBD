#!/bin/bash

size=$1

echo "Reading $size"
sleep_val=$2
echo $(cat /proc/sys/kernel/random/entropy_avail)
for i in `seq 10`
do
    start_S=$(cat /proc/sys/kernel/random/entropy_avail)
    if [ $size -gt 0 ];then
        head -c $size /dev/random > /dev/null
    fi
    sleep $sleep_val
    stop_S=$(cat /proc/sys/kernel/random/entropy_avail)
    delta=$(($stop_S-$start_S))
    echo "Delta entropy $(echo $delta/$sleep_val | bc -l)"
done
echo $(cat /proc/sys/kernel/random/entropy_avail)
