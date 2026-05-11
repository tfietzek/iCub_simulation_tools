#!/bin/bash

# starts two viewer for the iCub eyes

#### start right eye viewer 
echo 'start right eye viewer'
xterm -e 'yarpview --name /view/right; bash' &
echo "started right eye viewer" 

sleep 1

#### start left eye viewer 
echo 'start left eye viewer'
xterm -e 'yarpview --name /view/left; bash' &
echo "started left eye viewer" 

echo 'connect viewer'
xterm -e 'bash connect_viewer.sh; exit; bash' &
