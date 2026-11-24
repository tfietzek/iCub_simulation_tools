#!/bin/bash

# starts the gaze controller (iKinGazeCtrl) for the gazebo iCub; the simulator has to be started first
# note: with gz sim the eyes do not move correctly, since the controlboard plugin of gz-sim-yarp-plugins
# does not implement the mixed control mode used by iKinGazeCtrl for the eyes
# (https://github.com/robotology/gz-sim-yarp-plugins/issues/144); see demos/redball/head_gaze.py for an alternative


#### start GazeController Server
echo "run GazeController Server"
xterm -e 'iKinGazeCtrl --context gazeboCartesianControl --from iKinGazeCtrl.ini; bash' &
echo "started GazeController Server"
