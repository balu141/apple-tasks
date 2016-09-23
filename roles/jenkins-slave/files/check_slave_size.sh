#!/usr/bin/bash

guest_slave_size=$1
master_slave_size=$2

if [ $guest_slave_size -le $master_slave_size ]; then
    echo "less"
else
   echo "more"
fi
