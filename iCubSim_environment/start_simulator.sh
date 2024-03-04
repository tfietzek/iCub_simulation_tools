#!/bin/bash

# starts the yarpserver and the iCub simulator

#### start yarpserver
echo "run yarpserver"
xterm -e 'yarpserver --write; bash' &
echo "started yarpserver"
 
sleep 1

#### start iCub simulator
echo "run iCub_SIM" 
xterm -e 'iCub_SIM; bash' &
echo "started iCub_SIM"

