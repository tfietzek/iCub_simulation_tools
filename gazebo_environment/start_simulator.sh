#!/bin/bash

# starts the yarpserver and the gazebo simulator with the iCub inside

if [ $# == 0 ]
then
    file="./icub_image_visuomanip"

else
    file=$1
fi

#### start yarpserver
echo "run yarpserver"
xterm -e 'yarpserver --write; bash' &
echo "started yarpserver"
 
sleep 1

#### start iCub simulator
echo "run gazebo simulator" 
xterm -e "gazebo $file.world --verbose; bash" &
echo "started gazebo simulator"
