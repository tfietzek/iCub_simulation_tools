#!/bin/bash

# starts the programs for the Cartesian Controller -> Server and Client for the right arm


#### start CartesianControl Server
echo "run CartesianControl Server"
xterm -e 'yarprobotinterface --context gazeboCartesianControl; bash' &
echo "started CartesianControl Server"

sleep 10

#### start Cartesian Solver
#### start Cartesian Solver
if [ $1 ]
    then
        echo "run Cartesian Solver"
        xterm -e "iKinCartesianSolver --context gazeboCartesianControl --part $1 ; bash" &
        echo "started Cartesian Solver"
fi

if [ $2 ]
    then
        echo "run Cartesian Solver"
        xterm -e "iKinCartesianSolver --context gazeboCartesianControl --part $2 ; bash" &
        echo "started Cartesian Solver"
fi




