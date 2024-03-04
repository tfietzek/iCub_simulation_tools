#!/bin/bash

# starts the yarpserver, the iCub simulator, a viewer for the iCubs right eye and the dependent programs for the Cartesian Controller

#### start yarpserver
echo "run yarpserver"
xterm -e 'yarpserver --write; bash' &
echo "started yarpserver"
 
sleep 1

#### start iCub simulator
echo "run iCub_SIM" 
xterm -e 'iCub_SIM; bash' &
echo "started iCub_SIM"

sleep 1

#### start right eye viewer 
echo 'start right eye viewer'
xterm -e 'yarpview --name /view/right; bash' &
sleep 3
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

sleep 5

#### start CartesianControl Server
echo "run CartesianControl Server" 
xterm -e 'yarprobotinterface --context simCartesianControl; bash' &
echo "started CartesianControl Server"

sleep 10

#### start Cartesian Solver
if [ $1 ]
    then
        echo "run Cartesian Solver" 
        xterm -e "iKinCartesianSolver --context simCartesianControl --part $1 ; bash" &
        echo "started Cartesian Solver"
fi

if [ $2 ]
    then
        echo "run Cartesian Solver" 
        xterm -e "iKinCartesianSolver --context simCartesianControl --part $2 ; bash" &
        echo "started Cartesian Solver"
fi



