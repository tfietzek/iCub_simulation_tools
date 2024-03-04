
#### start skin gui
echo "start skin gui for right forearm"
xterm -e 'iCubSkinGui --from right_forearm.ini; bash' &
sleep 6

#### connect gui with simulator
xterm -e 'yarp connect /icubSim/skin/right_forearm_comp /skinGui/right_forearm:i;sleep 0.5; exit; bash' &
echo "started right eye viewer" 
