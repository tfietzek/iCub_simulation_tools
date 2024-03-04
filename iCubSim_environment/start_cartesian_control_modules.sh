#!/bin/bash

# starts the dependent programs for the Cartesian Controller

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
