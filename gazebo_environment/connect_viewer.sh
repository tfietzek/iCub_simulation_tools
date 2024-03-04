#!/bin/bash

# starts the yarpserver and the gazebo simulator with the iCub inside

#### connect viewer with camera
xterm -e 'yarp connect /icubSim/cam/right /view/right;sleep 0.5; exit; bash' &
xterm -e 'yarp connect /icubSim/cam/right/rgbImage:o /view/right;sleep 0.5; exit; bash' &
echo "connected right eye viewer" 

sleep 1

#### connect viewer with camera
xterm -e 'yarp connect /icubSim/cam/left /view/left;sleep 0.5; exit; bash' &
xterm -e 'yarp connect /icubSim/cam/left/rgbImage:o /view/left;sleep 0.5; exit; bash' &
echo "connected left eye viewer" 
