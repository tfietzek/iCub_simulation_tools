#!/bin/bash

# starts the yarpserver and the gazebo simulator with the iCub inside

if [ $# == 0 ]
then
    file="./icub_image_visuomanip"

else
    file=$1
fi

#### start yarpserver
echo "start simulator"
xterm -e "bash start_simulator.sh ${file}; exit; bash" &

sleep 1

#### start eye viewer
echo "start viewer"
xterm -e 'bash start_viewer.sh; exit; bash' &

    
