#!/bin/bash

# starts two viewer for the iCub eyes

#### start right eye viewer 
echo 'start right eye viewer'
xterm -e 'yarpview --name /view/right; bash' &
sleep 6
#### connect viewer with camera
xterm -e 'yarp connect /icubSim/cam/right /view/right;sleep 0.5; exit; bash' &
echo "started right eye viewer" 

sleep 1

#### start left eye viewer 
echo 'start left eye viewer'
xterm -e 'yarpview --name /view/left; bash' &
sleep 3
#### connect viewer with camera
xterm -e 'yarp connect /icubSim/cam/left /view/left;sleep 0.5; exit; bash' &
echo "started left eye viewer" 
