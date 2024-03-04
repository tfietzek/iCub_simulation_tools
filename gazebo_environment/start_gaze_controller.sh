#!/bin/bash

# starts the device for the Gazecontroller


#### start CartesianControl Server
echo "run GazeController Server" 
xterm -e 'iKinGazeCtrl --from configSim.ini; bash' &
echo "started GazeController Server"


